import { TwitterApi } from 'twitter-api-v2';
import { TwitterError } from './types.js';
export class TwitterClient {
    client;
    rateLimitMap = new Map();
    constructor(config) {
        this.client = new TwitterApi({
            appKey: config.apiKey,
            appSecret: config.apiSecretKey,
            accessToken: config.accessToken,
            accessSecret: config.accessTokenSecret,
        });
        console.error('Twitter API client initialized');
    }
    async postTweet(text) {
        try {
            const endpoint = 'tweets/create';
            await this.checkRateLimit(endpoint);
            const response = await this.client.v2.tweet(text);
            console.error(`Tweet posted successfully with ID: ${response.data.id}`);
            return {
                id: response.data.id,
                text: response.data.text
            };
        }
        catch (error) {
            this.handleApiError(error);
        }
    }
    async searchTweets(query, count) {
        try {
            const endpoint = 'tweets/search';
            await this.checkRateLimit(endpoint);
            const response = await this.client.v2.search(query, {
                max_results: count,
                expansions: ['author_id'],
                'tweet.fields': ['public_metrics', 'created_at'],
                'user.fields': ['username', 'name', 'verified']
            });
            console.error(`Fetched ${response.tweets.length} tweets for query: "${query}"`);
            const tweets = response.tweets.map(tweet => ({
                id: tweet.id,
                text: tweet.text,
                authorId: tweet.author_id ?? '',
                metrics: {
                    likes: tweet.public_metrics?.like_count ?? 0,
                    retweets: tweet.public_metrics?.retweet_count ?? 0,
                    replies: tweet.public_metrics?.reply_count ?? 0,
                    quotes: tweet.public_metrics?.quote_count ?? 0
                },
                createdAt: tweet.created_at ?? ''
            }));
            const users = response.includes.users.map(user => ({
                id: user.id,
                username: user.username,
                name: user.name,
                verified: user.verified ?? false
            }));
            return { tweets, users };
        }
        catch (error) {
            this.handleApiError(error);
        }
    }
    async checkRateLimit(endpoint) {
        const lastRequest = this.rateLimitMap.get(endpoint);
        if (lastRequest) {
            const timeSinceLastRequest = Date.now() - lastRequest;
            if (timeSinceLastRequest < 1000) { // Basic rate limiting
                throw new TwitterError('Rate limit exceeded', 'rate_limit_exceeded', 429);
            }
        }
        this.rateLimitMap.set(endpoint, Date.now());
    }
    handleApiError(error) {
        if (error instanceof TwitterError) {
            throw error;
        }
        // Handle twitter-api-v2 errors
        const apiError = error;
        if (apiError.code) {
            throw new TwitterError(apiError.message || 'Twitter API error', apiError.code, apiError.status);
        }
        // Handle unexpected errors
        console.error('Unexpected error in Twitter client:', error);
        throw new TwitterError('An unexpected error occurred', 'internal_error', 500);
    }
}
