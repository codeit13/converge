/**
 * Medium API MCP Server
 * A microservice for interacting with Medium's API to publish content and manage user accounts
 */

const express = require("express");
const axios = require("axios");
const cors = require("cors");
const bodyParser = require("body-parser");
const dotenv = require("dotenv");
const jwt = require("jsonwebtoken");
const mongoose = require("mongoose");
const rateLimit = require("express-rate-limit");
const { v4: uuidv4 } = require("uuid");
const crypto = require("crypto");
const morgan = require("morgan");
const redis = require("redis");
const { promisify } = require("util");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const TurndownService = require("turndown");
const showdown = require("showdown");
const winston = require("winston");

// Initialize environment variables
dotenv.config();

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;
const MEDIUM_API_URL = "https://api.medium.com/v1";

// Set up middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(morgan("combined"));

// Set up rate limiting
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: "Too many requests from this IP, please try again after 15 minutes",
});
app.use("/api/", apiLimiter);

// Set up storage for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, "uploads");
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir);
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  },
});
const upload = multer({ storage });

// Set up Redis for caching and queue management
let redisClient;
let getAsync;
let setAsync;

if (process.env.REDIS_URL) {
  redisClient = redis.createClient({
    url: process.env.REDIS_URL,
  });

  redisClient.on("error", (error) => {
    logger.error("Redis Error:", error);
  });

  getAsync = promisify(redisClient.get).bind(redisClient);
  setAsync = promisify(redisClient.set).bind(redisClient);
}

// Set up logging
const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: "medium-mcp" },
  transports: [
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" }),
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      ),
    }),
  ],
});

// Connect to MongoDB
mongoose
  .connect(process.env.MONGODB_URI || "mongodb://localhost:27017/medium-mcp", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    logger.info("Connected to MongoDB");
  })
  .catch((error) => {
    logger.error("MongoDB connection error:", error);
  });

// Define schemas
const UserSchema = new mongoose.Schema({
  userId: { type: String, required: true, unique: true },
  email: { type: String, required: true },
  name: { type: String },
  mediumId: { type: String },
  accessToken: { type: String },
  refreshToken: { type: String },
  tokenExpiry: { type: Date },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now },
});

const PostSchema = new mongoose.Schema({
  userId: { type: String, required: true },
  mediumPostId: { type: String },
  title: { type: String, required: true },
  content: { type: String, required: true },
  contentFormat: {
    type: String,
    enum: ["html", "markdown"],
    default: "markdown",
  },
  tags: [{ type: String }],
  canonicalUrl: { type: String },
  publishStatus: {
    type: String,
    enum: ["public", "draft", "unlisted"],
    default: "draft",
  },
  license: { type: String },
  publicationId: { type: String },
  scheduledAt: { type: Date },
  published: { type: Boolean, default: false },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now },
});

// Define models
const User = mongoose.model("User", UserSchema);
const Post = mongoose.model("Post", PostSchema);

// ============================
// Authentication Middleware
// ============================

const authenticateUser = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({ error: "Authentication required" });
    }

    const token = authHeader.split(" ")[1];
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    const user = await User.findOne({ userId: decoded.userId });

    if (!user) {
      return res.status(401).json({ error: "User not found" });
    }

    // Check if Medium token is expired and needs refresh
    if (user.tokenExpiry && new Date(user.tokenExpiry) < new Date()) {
      // Implement token refresh logic here if Medium API supports it
      logger.info(`Token expired for user ${user.userId}, attempting refresh`);

      // For now, just notify the user that re-authentication is needed
      return res
        .status(401)
        .json({
          error: "Medium authorization expired, please reconnect your account",
        });
    }

    req.user = user;
    next();
  } catch (error) {
    logger.error("Authentication error:", error);
    return res.status(401).json({ error: "Invalid or expired token" });
  }
};

// ============================
// Helper Functions
// ============================

const formatForMedium = (content, contentFormat) => {
  if (contentFormat === "markdown" && content) {
    // If content is in HTML but we need Markdown
    const turndownService = new TurndownService();
    return turndownService.turndown(content);
  } else if (contentFormat === "html" && content) {
    // If content is in Markdown but we need HTML
    const converter = new showdown.Converter();
    return converter.makeHtml(content);
  }
  return content;
};

const handleApiError = (error, res) => {
  logger.error("Medium API Error:", error);

  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    const status = error.response.status;
    const data = error.response.data;

    if (status === 429) {
      // Rate limiting
      return res.status(429).json({
        error: "Rate limited by Medium API",
        retryAfter: error.response.headers["retry-after"] || 60,
      });
    } else if (status === 401) {
      return res
        .status(401)
        .json({ error: "Medium authorization invalid or expired" });
    } else {
      return res.status(status).json({
        error: "Medium API error",
        details: data,
      });
    }
  } else if (error.request) {
    // The request was made but no response was received
    return res.status(503).json({ error: "Medium API unavailable" });
  } else {
    // Something happened in setting up the request that triggered an Error
    return res
      .status(500)
      .json({ error: "Internal server error", message: error.message });
  }
};

// ============================
// Auth Routes
// ============================

app.post("/api/auth/register", async (req, res) => {
  try {
    const { email, name } = req.body;

    if (!email) {
      return res.status(400).json({ error: "Email is required" });
    }

    const existingUser = await User.findOne({ email });

    if (existingUser) {
      return res.status(409).json({ error: "User already exists" });
    }

    const userId = uuidv4();

    const user = new User({
      userId,
      email,
      name: name || email.split("@")[0],
    });

    await user.save();

    const token = jwt.sign({ userId }, process.env.JWT_SECRET, {
      expiresIn: "7d",
    });

    res.status(201).json({
      message: "User registered successfully",
      token,
      user: {
        userId: user.userId,
        email: user.email,
        name: user.name,
      },
    });
  } catch (error) {
    logger.error("Registration error:", error);
    res
      .status(500)
      .json({ error: "Registration failed", message: error.message });
  }
});

app.post("/api/auth/login", async (req, res) => {
  try {
    const { email } = req.body;

    if (!email) {
      return res.status(400).json({ error: "Email is required" });
    }

    const user = await User.findOne({ email });

    if (!user) {
      return res.status(401).json({ error: "User not found" });
    }

    const token = jwt.sign({ userId: user.userId }, process.env.JWT_SECRET, {
      expiresIn: "7d",
    });

    res.status(200).json({
      message: "Login successful",
      token,
      user: {
        userId: user.userId,
        email: user.email,
        name: user.name,
        mediumConnected: !!user.mediumId,
      },
    });
  } catch (error) {
    logger.error("Login error:", error);
    res.status(500).json({ error: "Login failed", message: error.message });
  }
});

// Medium OAuth Routes
app.get("/api/auth/medium", authenticateUser, (req, res) => {
  const clientId = process.env.MEDIUM_CLIENT_ID;
  const redirectUri = process.env.MEDIUM_REDIRECT_URI;
  const state = crypto.randomBytes(16).toString("hex");

  // Store state in Redis for validation on callback
  if (redisClient) {
    setAsync(`medium_state:${req.user.userId}`, state, "EX", 3600); // 1 hour expiry
  }

  const authUrl = `https://medium.com/m/oauth/authorize?client_id=${clientId}&scope=basicProfile,publishPost&state=${state}&response_type=code&redirect_uri=${redirectUri}`;

  res.json({ authUrl });
});

app.get("/api/auth/medium/callback", async (req, res) => {
  try {
    const { code, state } = req.query;
    const userId = req.query.userId;

    if (!code || !state || !userId) {
      return res.status(400).json({ error: "Missing required parameters" });
    }

    // Validate state if Redis is available
    if (redisClient) {
      const storedState = await getAsync(`medium_state:${userId}`);
      if (storedState !== state) {
        return res.status(400).json({ error: "Invalid state parameter" });
      }
    }

    const user = await User.findOne({ userId });

    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    // Exchange the code for an access token
    const tokenResponse = await axios.post("https://api.medium.com/v1/tokens", {
      code,
      client_id: process.env.MEDIUM_CLIENT_ID,
      client_secret: process.env.MEDIUM_CLIENT_SECRET,
      grant_type: "authorization_code",
      redirect_uri: process.env.MEDIUM_REDIRECT_URI,
    });

    const { access_token, refresh_token, expires_at } = tokenResponse.data;

    // Get user details from Medium
    const userResponse = await axios.get(`${MEDIUM_API_URL}/me`, {
      headers: {
        Authorization: `Bearer ${access_token}`,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    const mediumUser = userResponse.data.data;

    // Update user with Medium details
    user.mediumId = mediumUser.id;
    user.accessToken = access_token;
    user.refreshToken = refresh_token || null;
    user.tokenExpiry = expires_at ? new Date(expires_at * 1000) : null;
    user.updatedAt = new Date();

    await user.save();

    res.redirect(`${process.env.FRONTEND_URL}/medium-connected?success=true`);
  } catch (error) {
    logger.error("Medium OAuth callback error:", error);
    res.redirect(
      `${
        process.env.FRONTEND_URL
      }/medium-connected?success=false&error=${encodeURIComponent(
        "Failed to connect Medium account"
      )}`
    );
  }
});

// ============================
// User Routes
// ============================

app.get("/api/user/profile", authenticateUser, async (req, res) => {
  try {
    res.json({
      userId: req.user.userId,
      email: req.user.email,
      name: req.user.name,
      mediumConnected: !!req.user.mediumId,
      mediumId: req.user.mediumId,
    });
  } catch (error) {
    logger.error("Get user profile error:", error);
    res
      .status(500)
      .json({ error: "Failed to get user profile", message: error.message });
  }
});

app.get("/api/user/medium-profile", authenticateUser, async (req, res) => {
  try {
    if (!req.user.mediumId || !req.user.accessToken) {
      return res.status(400).json({ error: "Medium account not connected" });
    }

    const response = await axios.get(`${MEDIUM_API_URL}/me`, {
      headers: {
        Authorization: `Bearer ${req.user.accessToken}`,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    res.json(response.data.data);
  } catch (error) {
    handleApiError(error, res);
  }
});

app.get("/api/user/publications", authenticateUser, async (req, res) => {
  try {
    if (!req.user.mediumId || !req.user.accessToken) {
      return res.status(400).json({ error: "Medium account not connected" });
    }

    const response = await axios.get(
      `${MEDIUM_API_URL}/users/${req.user.mediumId}/publications`,
      {
        headers: {
          Authorization: `Bearer ${req.user.accessToken}`,
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      }
    );

    res.json(response.data.data);
  } catch (error) {
    handleApiError(error, res);
  }
});

// ============================
// Posts Routes
// ============================

app.get("/api/posts", authenticateUser, async (req, res) => {
  try {
    const { status, page = 1, limit = 10 } = req.query;
    const skip = (page - 1) * limit;

    const query = { userId: req.user.userId };

    if (status) {
      query.publishStatus = status;
    }

    const posts = await Post.find(query)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Post.countDocuments(query);

    res.json({
      posts,
      total,
      page: parseInt(page),
      pages: Math.ceil(total / limit),
    });
  } catch (error) {
    logger.error("Get posts error:", error);
    res
      .status(500)
      .json({ error: "Failed to get posts", message: error.message });
  }
});

app.get("/api/posts/:postId", authenticateUser, async (req, res) => {
  try {
    const post = await Post.findOne({
      _id: req.params.postId,
      userId: req.user.userId,
    });

    if (!post) {
      return res.status(404).json({ error: "Post not found" });
    }

    res.json(post);
  } catch (error) {
    logger.error("Get post error:", error);
    res
      .status(500)
      .json({ error: "Failed to get post", message: error.message });
  }
});

app.post("/api/posts", authenticateUser, async (req, res) => {
  try {
    const {
      title,
      content,
      contentFormat = "markdown",
      tags,
      canonicalUrl,
      publishStatus = "draft",
      license,
      publicationId,
      scheduledAt,
    } = req.body;

    if (!title || !content) {
      return res.status(400).json({ error: "Title and content are required" });
    }

    const post = new Post({
      userId: req.user.userId,
      title,
      content,
      contentFormat,
      tags: tags || [],
      canonicalUrl,
      publishStatus,
      license,
      publicationId,
      scheduledAt: scheduledAt ? new Date(scheduledAt) : null,
    });

    await post.save();

    // If scheduled, add to the queue
    if (scheduledAt && redisClient) {
      const scheduleTime = new Date(scheduledAt).getTime();
      const now = Date.now();

      if (scheduleTime > now) {
        await setAsync(
          `post_schedule:${post._id}`,
          JSON.stringify({
            postId: post._id,
            userId: req.user.userId,
            scheduledAt,
          }),
          "EX",
          Math.floor((scheduleTime - now) / 1000)
        );

        logger.info(`Post ${post._id} scheduled for ${scheduledAt}`);
      }
    }

    // Publish immediately if requested
    if (publishStatus !== "draft" && !scheduledAt) {
      // Only attempt to publish if Medium account is connected
      if (req.user.mediumId && req.user.accessToken) {
        try {
          let publishEndpoint = `${MEDIUM_API_URL}/users/${req.user.mediumId}/posts`;

          // If publishing to a publication
          if (publicationId) {
            publishEndpoint = `${MEDIUM_API_URL}/publications/${publicationId}/posts`;
          }

          const formattedContent = formatForMedium(content, contentFormat);

          const publishData = {
            title,
            contentFormat: contentFormat === "html" ? "html" : "markdown",
            content: formattedContent,
            tags: tags || [],
            publishStatus,
            license: license || "",
          };

          if (canonicalUrl) {
            publishData.canonicalUrl = canonicalUrl;
          }

          const response = await axios.post(publishEndpoint, publishData, {
            headers: {
              Authorization: `Bearer ${req.user.accessToken}`,
              "Content-Type": "application/json",
              Accept: "application/json",
            },
          });

          const mediumPost = response.data.data;

          post.mediumPostId = mediumPost.id;
          post.published = true;
          await post.save();
        } catch (error) {
          logger.error("Medium publishing error:", error);
          // Continue anyway - we've saved the post locally
        }
      }
    }

    res.status(201).json(post);
  } catch (error) {
    logger.error("Create post error:", error);
    res
      .status(500)
      .json({ error: "Failed to create post", message: error.message });
  }
});
