<template>
  <div
    class="h-[90svh] w-full flex flex-row overflow-hidden relative"
    :style="{
      fontFamily: `'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif`,
    }"
  >
    <GoogleLogin :callback="oneTapGoogleLoginCallback" prompt>
      <span></span>
    </GoogleLogin>
    <!-- Overlay for mobile when sidebar is open -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-black/50 z-40 md:hidden"
      @click="toggleSidebar"
    ></div>

    <!-- Chat History Sidebar -->
    <div
      :class="[
        'transition-all duration-300 z-40 overflow-hidden',
        sidebarOpen
          ? 'border-r border-border fixed inset-y-0 left-0 md:static bg-background md:bg-transparent shadow-xl'
          : 'w-0 md:w-64',
      ]"
    >
      <ChatHistory :chatSessions="chatSessions" :isMobile="isMobile">
        <ScrollArea class="flex-1 p-2">
          <div class="space-y-2 overflow-hidden">
            <Button
              v-for="chat in chatSessions"
              :key="chat.chat_id"
              :variant="currentChatId === chat.chat_id ? 'secondary' : 'ghost'"
              class="w-full justify-start gap-2 text-left"
              @click="
                loadChat(chat.chat_id);
                closeSidebarOnMobile();
              "
            >
              <MessageSquare class="h-4 w-4" />
              <div class="flex-1 truncate">
                {{ chat.title || "Untitled Chat" }}
              </div>
              <Button
                v-if="currentChatId === chat.chat_id"
                variant="ghost"
                size="icon"
                class="h-4 w-4 hover:bg-destructive/20 hover:text-destructive"
                @click.stop="deleteCurrentChat"
              >
                <Trash2 class="h-3 w-3" />
              </Button>
            </Button>
          </div>
        </ScrollArea>
      </ChatHistory>
    </div>

    <Card
      class="flex-1 flex flex-col overflow-hidden shadow-lg border-none m-0 rounded-none md:ml-0 w-full bg-transparent"
      :class="{ 'ml-1': !sidebarOpen }"
    >
      <CardHeader class="border-b py-3 md:py-4 px-0 md:px-6">
        <div
          v-motion="{
            initial: { opacity: 0, y: -20 },
            enter: { opacity: 1, y: 0, transition: { duration: 500 } },
          }"
          class="flex items-center justify-between w-full"
        >
          <div class="flex items-center gap-4">
            <!-- Sidebar toggle visible on all screen sizes -->
            <Button
              variant="outline"
              size="icon"
              class="h-8 w-8 flex md:hidden text-primary border-none hover:bg-primary/10"
              @click="toggleSidebar"
            >
              <History v-if="!sidebarOpen" class="h-4 w-4" />
              <X v-else class="h-4 w-4" />
            </Button>
            <Bot class="h-5 w-5 md:h-6 md:w-6 text-primary hidden md:block" />
            <div>
              <CardTitle class="font-display text-lg md:text-xl">
                Chat with AI
              </CardTitle>
            </div>
          </div>
          <Button
            variant="outline"
            size="sm"
            class="text-xs md:text-sm border-primary/20 hover:bg-primary/10 text-primary"
            @click="createNewChat"
          >
            <Plus class="h-3 w-3 mr-1" />
            New Chat
          </Button>
        </div>
      </CardHeader>

      <CardContent
        class="flex-1 overflow-y-auto px-1.5 py-6 md:p-6 md:mx-auto md:max-w-full lg:max-w-full xl:max-w-7xl space-y-6 custom-scrollbar"
        id="chat-container"
        ref="chatContainer"
        external-links
      >
        <!-- Welcome message -->
        <div
          v-if="messages.length === 0"
          v-motion="{
            initial: { opacity: 0, scale: 0.9 },
            enter: {
              opacity: 1,
              scale: 1,
              transition: { duration: 700, delay: 300 },
            },
          }"
          class="flex flex-col items-center justify-center h-full text-center space-y-8 text-muted-foreground py-8"
        >
          <div class="rounded-full bg-primary/10 p-6">
            <img src="/images/logo.png" class="h-12 w-12" />
          </div>
          <div>
            <h3 class="text-xl font-display font-medium mb-3">
              Start a conversation
            </h3>
            <p class="text-muted-foreground mb-6">
              Ask a question or give an instruction to begin writing an article
            </p>

            <!-- Example prompts that auto-send when clicked -->
            <div
              class="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto mt-6 px-4"
            >
              <Button
                v-for="(prompt, index) in examplePrompts"
                :key="index"
                variant="outline"
                class="p-4 h-auto text-sm text-left justify-start hover:border-primary/50 hover:bg-primary/5 group border-border/60"
                @click="sendExamplePrompt(prompt)"
              >
                <div>
                  <p class="font-medium text-primary mb-1 flex items-center">
                    <SparklesIcon class="h-3 w-3 mr-2 text-primary/70" />
                    {{ prompt.title }}
                  </p>
                  <p
                    class="text-muted-foreground text-xs line-clamp-2 group-hover:text-foreground/90 transition-colors whitespace-normal"
                  >
                    {{ prompt.text }}
                  </p>
                </div>
              </Button>
            </div>
          </div>
        </div>

        <div
          v-for="(message, index) in messages"
          :key="index"
          class="flex flex-col space-y-4"
        >
          <!-- User message -->
          <div
            v-if="message.role === 'user'"
            v-motion="{
              initial: { opacity: 0, x: 20 },
              enter: { opacity: 1, x: 0, transition: { duration: 300 } },
            }"
            class="flex items-start gap-3 rounded-lg ml-auto max-w-[90%] md:max-w-[85%] lg:max-w-[80%] px-1"
          >
            <div
              class="rounded-2xl p-3.5 shadow-sm break-words w-full min-w-[150px] bg-primary/5 backdrop-blur-sm border border-primary/10"
            >
              <p
                class="prose prose-sm max-w-none dark:prose-invert text-foreground/90 tracking-wide leading-relaxed"
              >
                {{ message.content }}
              </p>
            </div>
            <Avatar class="h-8 w-8 shrink-0">
              <AvatarImage src="" />
              <AvatarFallback>
                <User class="h-4 w-4" />
              </AvatarFallback>
            </Avatar>
          </div>

          <!-- AI message -->
          <div
            v-else-if="message.role === 'assistant'"
            v-motion="{
              initial: { opacity: 0, x: -20 },
              enter: { opacity: 1, x: 0, transition: { duration: 300 } },
            }"
            class="flex items-start gap-3 max-w-[98%] md:max-w-[90%] lg:max-w-[90%] px-1"
          >
            <Avatar class="h-8 w-8 shrink-0">
              <AvatarImage src="" />
              <AvatarFallback class="bg-secondary text-secondary-foreground">
                <Bot class="h-4 w-4" />
              </AvatarFallback>
            </Avatar>
            <div class="flex flex-col w-full">
              <!-- Thinking section - collapsible -->
              <div
                v-if="message.thinking && message.thinking.length > 0"
                class="w-full h-fit"
              >
                <div
                  class="flex items-center gap-2 px-3 py-1.5 cursor-pointer transition-colors rounded-lg hover:bg-secondary/5"
                  @click="toggleThinking(message)"
                >
                  <span class="text-sm font-medium text-muted-foreground/70">
                    {{
                      message?.thinkingTime
                        ? "Thought for"
                        : "Reasoning & Tools"
                    }}
                    <span
                      v-if="message.thinkingTime"
                      class="ml-0.5 font-medium text-muted-foreground/80"
                    >
                      {{ formatTime(message.thinkingTime) }}
                    </span>
                  </span>
                  <ChevronDown
                    class="h-3.5 w-3.5 ml-auto transition-transform text-muted-foreground"
                    :class="{ 'rotate-180': message.showThinking }"
                  />
                </div>
                <div
                  class="relative rounded-lg px-3 py-0 mt-2 text-sm bg-background/5 transition-all duration-2000"
                  :class="{
                    'h-0 overflow-hidden': !message.showThinking,
                  }"
                >
                  <div
                    class="bg-primary/10 absolute top-1 left-0 w-1 h-full rounded-full"
                  ></div>
                  <div
                    v-for="(step, i) in message.thinking"
                    :key="`thinking-${i}`"
                    class="mb-1 ml-2"
                  >
                    <div class="flex items-center gap-2">
                      <!-- <div class="rounded-full p-1 bg-primary/5">
                        <Lightbulb class="h-3 w-3 text-muted-foreground" />
                      </div> -->
                      <div class="font-medium text-sm break-words">
                        <span v-if="step.type === 'thinking'">
                          {{ step.data }}
                        </span>
                        <span
                          v-else-if="step.type === 'tool_calls'"
                          class="text-secondary"
                        >
                          Calling
                          {{
                            step.data
                              .map((tool) =>
                                tool
                                  .replace(/_/g, " ")
                                  .replace(/(^|\s)\S/g, (l) => l.toUpperCase())
                              )
                              .join(", ")
                          }}
                          {{
                            (step?.data || []).length == 1 ? "tool " : "tools: "
                          }}
                        </span>

                        <div
                          v-else-if="step.type === 'tool_messages'"
                          class="text-sm font-medium text-muted-foreground break-words text-wrap"
                        >
                          <span v-html="step.data"></span>
                        </div>

                        <!-- Format JSON content nicely -->
                        <div
                          v-if="
                            step.data &&
                            typeof step.data === 'object' &&
                            !['tool_calls', 'tool_messages'].includes(step.type)
                          "
                          class="space-y-2 px-4 py-2 mb-2 border border-muted/50 rounded-md"
                        >
                          <div
                            v-for="(value, key) in step.data"
                            :key="key"
                            class="flex items-start gap-2"
                          >
                            <span
                              class="font-medium text-sm text-muted-foreground capitalize"
                            >
                              {{
                                typeof key === "number"
                                  ? key + 1
                                  : Number.isNaN(parseInt(key))
                                  ? key
                                  : parseInt(key) + 1
                              }}:
                            </span>
                            <div class="flex-1">
                              <!-- Handle different types of values -->
                              <div
                                v-if="
                                  typeof value === 'object' && value !== null
                                "
                              >
                                <ul class="list-disc list-inside space-y-1">
                                  <li
                                    v-for="(item, idx) in Array.isArray(value)
                                      ? value
                                      : Object.values(value)"
                                    :key="idx"
                                    class="text-sm text-muted-foreground"
                                  >
                                    {{ item }}
                                  </li>
                                </ul>
                              </div>
                              <div v-else class="text-sm text-muted-foreground">
                                {{ value }}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Message content -->
              <div
                class="group relative rounded-lg px-0 py-1 md:py-0 md:px-4 break-words w-full backdrop-blur-sm"
                :class="{
                  'bg-secondary/0': message.role === 'assistant',
                  'bg-secondary': message.role === 'user',
                }"
              >
                <div
                  v-if="message.content"
                  v-html="formatMessage(message)"
                  class="prose prose-sm max-w-none dark:prose-invert text-foreground/90 tracking-wide leading-relaxed custom-scrollbar rounded-2xl p-3.5 shadow-sm break-words w-full min-w-[150px] bg-primary/5 backdrop-blur-sm border border-primary/10"
                ></div>
                <div
                  v-else
                  class="animate-bounce flex items-center space-x-2 pt-2 pb-3 ml-6 md:ml-0 md:mt-4 md:pt-0"
                >
                  <span
                    class="font-xs tracking-wide text-normal text-muted-foreground"
                  >
                    Thinking
                  </span>
                  <div class="flex space-x-1">
                    <span
                      class="animate-bounce delay-150 h-1.5 w-1.5 rounded-full bg-muted-foreground/70"
                    ></span>
                    <span
                      class="animate-bounce delay-300 h-1.5 w-1.5 rounded-full bg-muted-foreground/70"
                    ></span>
                    <span
                      class="animate-bounce delay-500 h-1.5 w-1.5 rounded-full bg-muted-foreground/70"
                    ></span>
                  </div>
                </div>

                <!-- Message actions -->
                <div
                  class="absolute -top-2 right-2 opacity-0 group-hover:opacity-100 focus-within:opacity-100 transition-opacity duration-200 flex space-x-1 bg-background/70 backdrop-blur-sm rounded-md shadow-sm border border-muted/10 p-0.5"
                >
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="copyToClipboard(message.content)"
                    class="h-6 w-6"
                    title="Copy message"
                  >
                    <Copy class="h-3 w-3 text-muted-foreground" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="regenerateResponse(message)"
                    class="h-6 w-6"
                    title="Regenerate response"
                  >
                    <RefreshCw class="h-3 w-3 text-muted-foreground" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="saveToNotes(message)"
                    class="h-6 w-6"
                    title="Save to notes"
                  >
                    <Save class="h-3 w-3 text-muted-foreground" />
                  </Button>
                </div>
              </div>
            </div>
          </div>

          <!-- System message -->
          <div
            v-else-if="message.role === 'system'"
            v-motion="{
              initial: { opacity: 0, y: 10 },
              enter: { opacity: 1, y: 0, transition: { duration: 300 } },
            }"
            class="flex justify-center"
          >
            <div
              class="rounded-full bg-accent/20 text-accent-foreground px-4 py-1.5 text-sm font-medium"
            >
              <p>{{ message.content }}</p>
            </div>
          </div>
        </div>
      </CardContent>

      <!-- Input area -->
      <div
        class="sticky bottom-0 max-w-[98%] md:max-w-[70vw] lg:max-w-[70vw] xl:max-w-[70vw] mx-auto w-full backdrop-blur-sm z-10"
      >
        <!-- Response type toggle and options -->
        <div
          class="flex items-center justify-start md:justify-end md:mr-14 px-1 overflow-x-auto custom-scrollbar"
        >
          <div class="flex gap-2 pb-2">
            <div class="flex items-center gap-2 mr-2">
              <Wrench class="h-4 w-4 text-muted-foreground" />
              <span class="text-sm font-medium">Tools</span>
            </div>
            <div class="flex gap-2 overflow-x-auto whitespace-nowrap">
              <Badge
                v-for="tool in availableTools"
                :key="tool.name"
                variant="secondary"
                class="px-2 md:px-2.5 cursor-help transition-colors hover:bg-secondary/80"
                :title="tool.description"
              >
                {{ tool.name .replace(/_/g, " ") .replace(/(?<!^)[A-Z][a-z]+/g, (match) =>
                ` ${match}`) .replace(/(^|\s)\S/g, (l) => l.toUpperCase()) }}
              </Badge>
            </div>
          </div>
        </div>

        <form
          @submit.prevent="sendMessage"
          class="flex items-center justify-center"
        >
          <div class="relative flex-1 items-center justify-center">
            <Textarea
              v-model="userInput"
              placeholder="Type a message..."
              class="resize-none border-muted/30 focus:border-primary/40 bg-background/90 min-h-[60px] md:min-h-[80px] backdrop-blur-sm py-3 pl-4 pr-[90px] rounded-xl shadow-inner custom-scrollbar"
              @keydown="handleEnterKey"
              ref="textarea"
            ></Textarea>
            <div
              class="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center gap-1"
            >
              <Button
                v-if="userInput.trim().length > 0"
                type="button"
                variant="ghost"
                size="icon"
                class="opacity-70 hover:opacity-100 transition-opacity h-8 w-8"
                @click="userInput = ''"
              >
                <X class="h-4 w-4" />
              </Button>
              <Button
                type="submit"
                :disabled="isLoading || userInput.trim().length === 0"
                class="h-8 w-8 p-0 bg-primary hover:bg-primary/90 transition-colors"
                v-motion:hover="{
                  scale: 1.05,
                  transition: { type: 'spring', stiffness: 300, damping: 15 },
                }"
              >
                <Send class="h-4 w-4" />
              </Button>
            </div>
          </div>
        </form>
      </div>
    </Card>
  </div>
</template>

<script setup>
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardFooter,
  CardTitle,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import Input from "@/components/ui/input/Input.vue";
import Textarea from "@/components/ui/textarea/Textarea.vue";
import {
  Bot,
  ChevronDown,
  ChevronUp,
  Copy,
  ExternalLink,
  Lightbulb,
  History,
  MessageSquare,
  Plus,
  RefreshCw,
  Save,
  Send,
  SparklesIcon,
  Trash2,
  User,
  X,
  Wrench,
  Clock,
} from "lucide-vue-next";

// Import ChatHistory component
import ChatHistory from "@/components/chat/ChatHistory.vue";
</script>

<script>
// Component imports

import DOMPurify from "dompurify";
import { marked } from "marked";
import { mapState } from "vuex";

export default {
  name: "Chat",
  data() {
    return {
      isOneTapPromptEnabled: location.href.includes("localhost") ? false : true,
      userInput: "",
      messages: [],
      isLoading: false,
      lastUserMessage: "",
      useStreaming: true,
      currentChatId: null,
      intervalId: null,
      isTyping: false,
      showThinking: {},
      responseType: "streaming", // or "thinking"
      showResponseOptions: false,
      sidebarOpen: false, // Controls mobile sidebar visibility
      isMobile: window.innerWidth < 768, // Used for responsive behavior
      // Example prompts for empty chat
      examplePrompts: [
        {
          title: "Article on Latest AI news",
          text: "Write an article on what's currently happening in AI related to coding, provide insights and analysis.",
        },
        {
          title: "Generate code",
          text: "Write a JavaScript function to find the most frequent element in an array.",
        },
      ],
    };
  },
  computed: {
    ...mapState(["availableTools"]),
    latestAiMessage() {
      const aiMessages = this.messages.filter(
        (message) => message.role === "assistant"
      );
      return aiMessages[aiMessages.length - 1] || null;
    },
    userId() {
      return this.$store.state?.auth?.user?._id || "1" || 1;
    },
    chatSessions() {
      return this.$store.state.chatSessions || [];
    },
  },
  watch: {
    messages: {
      deep: true,
      handler() {
        // this.scrollToBottom();
      },
    },
    propName: {
      immediate: true,
      handler(newVal, oldVal) {
        // Handle prop changes
      },
    },
  },
  async mounted() {
    this.$store.dispatch("getAvailableTools");
    // Add event listener for Ctrl+K
    document.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        this.$refs.textarea?.focus();
      }
    });

    // Load chat sessions
    await this.$store.dispatch("getChatSessions");

    // Set focus on input
    // if (this.$refs.messageInput) {
    //   this.$refs.messageInput.focus();
    // }

    // Initialize Google One Tap if enabled
    if (this.isOneTapPromptEnabled && !this.$store.state.auth.user) {
      window.google?.accounts.id.initialize({
        client_id: process.env.VUE_APP_GOOGLE_CLIENT_ID,
        callback: this.oneTapGoogleLoginCallback,
      });
      window.google?.accounts.id.prompt();
    }

    // Scroll to bottom
    this.scrollToBottom();
  },
  unmounted() {
    clearInterval(this.intervalId);
    window.removeEventListener("resize", this.handleResize);
  },
  methods: {
    async oneTapGoogleLoginCallback(response) {
      if (response.credential) {
        await this.$store.dispatch("auth/loginViaGoogle", {
          idToken: response.credential,
        });
        await this.$store.dispatch("auth/getUserProfile");
      } else {
        await this.$store.dispatch("auth/loginViaGoogle", {
          code: response.code,
        });
        await this.$store.dispatch("auth/getUserProfile");
      }
    },
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },

    closeSidebarOnMobile() {
      // Close sidebar automatically on mobile after selecting a chat
      if (window.innerWidth < 768) {
        // md breakpoint
        this.sidebarOpen = false;
      }
    },

    sendExamplePrompt(prompt) {
      if (this.isLoading) return;

      // Set the prompt text as user input
      this.userInput = prompt.text;

      // Send the message
      this.sendMessage();
    },

    openLink(link) {
      window.open(link, "_blank");
    },
    async createNewChat() {
      try {
        // Get user ID from store
        const userId = this.$store.state.auth.user?._id || "1";
        if (!userId) {
          throw new Error("User not authenticated");
        }

        // Create new chat with user ID
        const response = await this.$store.dispatch("createChat", {
          user_id: userId,
        });
        if (!response?.data?.chat_id) {
          throw new Error("Failed to create chat: Invalid response");
        }

        console.log("Created new chat session with ID:", response.data.chat_id);
        this.currentChatId = response.data.chat_id;
        this.messages = [];
        this.userInput = "";
        this.lastUserMessage = "";
        this.isLoading = false;
        return response.data;
      } catch (error) {
        console.error("Error creating chat:", error);
        this.$store.commit("SET_TOASTER_DATA", {
          message: "Failed to create chat: " + error.message,
          type: "error",
        });
        return null;
      }
      await this.$store.dispatch("getChatSessions");
    },

    async loadChat(chatId) {
      this.currentChatId = chatId;
      const messages = await this.$store.dispatch("getChatMessages", chatId);
      this.messages = messages;
      this.scrollToBottom();
    },

    async deleteCurrentChat() {
      if (this.currentChatId) {
        await this.$store.dispatch("deleteChat", this.currentChatId);
        // this.createNewChat();
      }
    },
    clearChat() {
      this.messages = [
        {
          role: "system",
          content: "Conversation started",
        },
      ];
      this.userInput = "";
      this.isLoading = false;
    },
    copyConversation() {
      const formattedConversation = this.messages
        .filter((message) => message.role !== "system")
        .map((message) => {
          const role = message.role === "user" ? "User" : "AI";
          return `${role}: ${message.content}`;
        })
        .join("\n\n");

      this.copyToClipboard(formattedConversation);
    },
    toggleThinking(message) {
      if (message.thinking && message.thinking.length > 0) {
        message.showThinking = !message.showThinking;
      }
    },
    async sendMessage() {
      // Don't proceed if no input or already loading
      if (!this.userInput.trim() || this.isLoading) return;

      const userMessage = this.userInput.trim();
      this.userInput = "";
      this.isLoading = true;

      try {
        // Get or create chat ID
        if (!this.currentChatId) {
          const newChat = await this.createNewChat();
          if (!newChat?.chat_id) {
            throw new Error("Failed to create chat session");
          }
          this.currentChatId = newChat.chat_id;
        }

        // Add user message
        this.messages.push({
          role: "user",
          content: userMessage,
          timestamp: new Date().toISOString(),
        });

        // Add assistant message placeholder
        const assistantMessage = {
          role: "assistant",
          content: "",
          thinking: [],
          timestamp: new Date().toISOString(),
          thinkingStartTime: Date.now(),
          showThinking: true,
        };
        this.messages.push(assistantMessage);
        this.scrollToBottom();
        this.lastUserMessage = userMessage;

        // Choose between streaming and non-streaming API
        if (this.useStreaming) {
          // Use streaming API
          await this.$store.dispatch("streamAgent", {
            userPrompt: userMessage,
            chatId: this.currentChatId,
            onMessage: this.onMessage,
            onError: this.onError,
            onComplete: this.onComplete,
          });
        } else {
          // Use non-streaming API
          const response = await this.$store.dispatch("runAgent", userMessage);
          if (response?.data) {
            this.messages[this.messages.length - 1].content =
              response.data.content;
          }
          this.isLoading = false;
        }
      } catch (error) {
        console.error("Error in sendMessage:", error);

        // Check if we need to add an error message
        if (
          this.messages.length > 0 &&
          this.messages[this.messages.length - 1].role === "assistant"
        ) {
          this.messages[
            this.messages.length - 1
          ].content = `Seems like our servers are taking a coffee break. Please try again after the break :)

${error}`;
        } else {
          this.messages.push({
            role: "system",
            content: "Failed to send message. Please try again.",
            timestamp: new Date().toISOString(),
          });
        }

        this.isLoading = false;
        this.scrollToBottom();
      }
    },
    onMessage(data) {
      console.log("Stream data:", data);
      // Process each stream message based on type
      if (data.type === "thinking") {
        const thinking = data?.data || [];
        this.messages[this.messages.length - 1].thinking.push({
          type: "thinking",
          data: thinking,
        });
        this.scrollToBottom();
      } else if (data.type === "tool_calls") {
        const tools = data?.data || [];
        this.messages[this.messages.length - 1].thinking.push({
          type: "tool_calls",
          data: tools,
        });
        this.scrollToBottom();
      } else if (data.type === "tool_messages") {
        const message = data?.data?.messages[data?.data?.messages.length - 1];
        if (message) {
          let messageContent = message?.content;
          if (typeof messageContent === "object") {
            messageContent = JSON.stringify(messageContent, null, 2);
          }
          this.messages[this.messages.length - 1].thinking.push({
            type: "tool_messages",
            data: messageContent,
          });
          this.scrollToBottom();
        }
      } else if (data.type === "stream") {
        // Update AI response content
        const currentMessage = this.messages[this.messages.length - 1];
        currentMessage.content += data.data;
        this.scrollToBottom();
      } else if (data.type === "chunk" && data.data && data.data !== "") {
        let chunk = data.data;
        try {
          chunk = JSON.parse(chunk);
        } catch (e) {
          console.log(
            "Seems like chunk is already a valid string, processing it"
          );
        }
        // Handle direct message chunks
        if (typeof chunk === "object" && chunk.message_to_user) {
          this.messages[this.messages.length - 1].content =
            chunk.message_to_user;
        } else {
          this.messages[this.messages.length - 1].content = chunk;
        }
        this.scrollToBottom();
      } else if (data.type === "complete") {
        const article = data?.data?.article;
        messageStr = !this.messages[this.messages.length - 1].content || "";
        if (!messageStr.includes(article?.link)) {
          if (article && article?.link) {
            this.messages[this.messages.length - 1].content += `

Article is now live at ${article.link}`;
          }
        }
      } else if (data.type === "error") {
        this.messages[
          this.messages.length - 1
        ].content = `Seems like our servers are taking a coffee break. Please try again after the break :)

${data.data}`;
        this.isLoading = false;
        this.scrollToBottom();
      }
    },
    onError(error) {
      console.error("Streaming error:", error);
      this.messages[
        this.messages.length - 1
      ].content = `Seems like our servers are taking a coffee break. Please try again after the break :)

${error}`;
      this.isLoading = false;
      this.scrollToBottom();
    },
    onComplete() {
      this.isLoading = false;
      const lastMessage = this.messages[this.messages.length - 1];
      if (lastMessage) {
        // Calculate thinking time
        const endTime = Date.now();
        const thinkingTime = Math.round(
          (endTime - lastMessage.thinkingStartTime) / 1000
        );
        lastMessage.thinkingTime = thinkingTime;
        // Auto collapse thinking when complete
        setTimeout(() => {
          if (lastMessage) {
            lastMessage.showThinking = false;
          }
        }, 1000);
      }
      this.scrollToBottom();
    },
    handleEnterKey(e) {
      // If Enter is pressed without Shift, send the message
      if (!e.shiftKey && e.key === "Enter" && this.userInput.trim()) {
        this.sendMessage();
        e.preventDefault();
        return;
      }

      // If Shift+Enter is pressed, add a new line
      if (e.shiftKey && e.key === "Enter") {
        const input = this.$refs.textarea?.$el?.querySelector("textarea");
        if (!input) return;

        const start = input.selectionStart || 0;
        const end = input.selectionEnd || 0;
        this.userInput =
          this.userInput.substring(0, start) +
          "\n" +
          this.userInput.substring(end);
        input.selectionStart = input.selectionEnd = start + 1;
        e.preventDefault();
      }
    },
    scrollToBottom() {
      const container = document.getElementById("chat-container");
      if (container) {
        container.scrollTo({
          top: container.scrollHeight,
          behavior: "smooth",
        });

        setTimeout(() => {
          container.scrollTo({
            top: container.scrollHeight,
            behavior: "smooth",
          });
        }, 100);
      }

      setTimeout(() => {
        try {
          document.querySelectorAll("a").forEach((anchor) => {
            if (
              !anchor.hasAttribute("target") ||
              anchor.getAttribute("target") !== "_blank"
            ) {
              anchor.setAttribute("target", "_blank");
              anchor.setAttribute("rel", "noopener noreferrer");
            }
          });
        } catch (e) {
          console.log(e);
        }
      }, 500);
    },
    formatMessage(message) {
      let content = message?.content ?? "";
      if (!content) return "";

      // Configure marked to add classes to code blocks
      const renderer = new marked.Renderer();
      renderer.code = (code, language) => {
        return `<div class="code-block-wrapper"><pre class="language-${
          language || "text"
        }"><code class="language-${
          language || "text"
        }">${code}</code></pre></div>`;
      };

      // Apply syntax highlighting to inline code
      renderer.codespan = (code) => {
        return `<code class="inline-code">${code}</code>`;
      };

      const options = {
        renderer,
        highlight: function (code, lang) {
          return code; // We'll rely on CSS for styling
        },
        breaks: true,
        gfm: true,
      };

      const html = marked.parse(content, options);
      return DOMPurify.sanitize(html);
    },
    formatTime(seconds) {
      if (seconds < 60) {
        return `${seconds}s`;
      }
      if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60);
        return `${minutes}m`;
      }
      if (seconds < 86400) {
        const hours = Math.floor(seconds / 3600);
        return `${hours}hr`;
      }
      return "0s";
    },
    copyToClipboard(text) {
      if (!text) return;

      navigator.clipboard
        .writeText(text)
        .then(() => {
          this.$store.commit("SET_TOASTER_DATA", {
            message: "Copied to clipboard",
            type: "success",
            show: true,
          });
        })
        .catch((err) => {
          console.error("Failed to copy text:", err);
          this.$store.commit("SET_TOASTER_DATA", {
            message: "Failed to copy text",
            type: "error",
            show: true,
          });
        });
    },
    // Handle window resize to detect mobile/desktop view
    handleResize() {
      this.isMobile = window.innerWidth < 768;
    },
    regenerateResponse(message) {
      if (this.isLoading) return;

      // If specific message provided
      if (message) {
        const index = this.messages.indexOf(message);
        if (index !== -1 && index > 0) {
          // Find preceding user message
          for (let i = index - 1; i >= 0; i--) {
            if (this.messages[i].role === "user") {
              // Remove AI message
              this.messages.splice(index, 1);
              // Set user input and resend
              this.userInput = this.messages[i].content;
              this.sendMessage();
              return;
            }
          }
        }
      }

      // Fallback to last user message
      if (this.lastUserMessage) {
        if (this.latestAiMessage) {
          const index = this.messages.indexOf(this.latestAiMessage);
          if (index !== -1) {
            this.messages.splice(index, 1);
          }
        }
        this.userInput = this.lastUserMessage;
        this.sendMessage();
      }
    },
    saveToNotes(message) {
      const content =
        (message && message.content) ||
        (this.latestAiMessage && this.latestAiMessage.content);
      if (!content) return;

      this.$store.commit("SET_TOASTER_DATA", {
        message: "Response saved to notes",
        type: "success",
        show: true,
      });

      // Actual save functionality would be implemented here
      // e.g.: this.$store.dispatch('saveToNotes', content);
    },
    toggleResponseType() {
      this.useStreaming = !this.useStreaming;
      this.$store.commit("SET_TOASTER_DATA", {
        type: "info",
        message: this.useStreaming
          ? "Streaming enabled"
          : "Regular mode enabled",
        description: this.useStreaming
          ? "You'll now see the agent's thinking process in real-time."
          : "Responses will be shown only when fully complete.",
      });
    },
  },
};
</script>

<style scoped>
/* Improved scrollbars */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
}

/* Code block styling */
:deep(.code-block-wrapper) {
  position: relative;
  overflow-x: auto;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.5rem;
  margin: 1rem 0;
}

:deep(pre) {
  padding: 1rem;
  overflow-x: auto;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.2) !important;
  font-family: "JetBrains Mono", Menlo, Monaco, Consolas, "Liberation Mono",
    "Courier New", monospace;
  font-size: 0.85rem;
  line-height: 1.5;
  tab-size: 2;
  -moz-tab-size: 2;
}

:deep(pre code) {
  font-family: inherit;
  padding: 0;
  background: transparent !important;
  white-space: pre;
  word-break: normal;
  overflow-wrap: normal;
  color: rgba(255, 255, 255, 0.9);
}

:deep(.inline-code) {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.25rem;
  padding: 0.1rem 0.3rem;
  font-family: "JetBrains Mono", Menlo, Monaco, Consolas, "Liberation Mono",
    "Courier New", monospace;
  font-size: 0.85em;
  color: rgba(255, 255, 255, 0.9);
}

/* Text content styling */
:deep(p) {
  margin-bottom: 1rem;
  line-height: 1.6;
}

:deep(ul),
:deep(ol) {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

:deep(li) {
  margin-bottom: 0.5rem;
}

:deep(a) {
  color: #0ea5e9;
  text-decoration: none;
  border-bottom: 1px dotted currentColor;
}

:deep(a:hover) {
  border-bottom: 1px solid currentColor;
}

:deep(blockquote) {
  border-left: 4px solid rgba(255, 255, 255, 0.2);
  padding-left: 1rem;
  font-style: italic;
  color: rgba(255, 255, 255, 0.7);
  margin: 1rem 0;
}

:deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  overflow-x: auto;
  display: block;
}

:deep(th),
:deep(td) {
  padding: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  text-align: left;
}

:deep(th) {
  background: rgba(255, 255, 255, 0.05);
}

:deep(tr:nth-child(even)) {
  background: rgba(255, 255, 255, 0.03);
}

/* Animation styles */
.typing-animation {
  display: inline-flex;
  align-items: center;
  height: 1.5rem;
}

.typing-dot {
  display: inline-block;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  margin: 0 1px;
  background: currentColor;
  animation: typingAnimation 1.4s infinite ease-in-out;
  opacity: 0.6;
}

.typing-dot:nth-child(1) {
  animation-delay: 0s;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingAnimation {
  0%,
  100% {
    transform: scale(0.7);
    opacity: 0.2;
  }
  50% {
    transform: scale(1);
    opacity: 0.8;
  }
}
</style>
