import { z } from 'zod';
// Configuration schema with validation
export const ConfigSchema = z.object({
    apiKey: z.string().min(1, 'API Key is required'),
    apiSecretKey: z.string().min(1, 'API Secret Key is required'),
    accessToken: z.string().min(1, 'Access Token is required'),
    accessTokenSecret: z.string().min(1, 'Access Token Secret is required')
});
// Tool input schemas
export const PostTweetSchema = z.object({
    text: z.string()
        .min(1, 'Tweet text cannot be empty')
        .max(280, 'Tweet cannot exceed 280 characters')
});
export const SearchTweetsSchema = z.object({
    query: z.string().min(1, 'Search query cannot be empty'),
    count: z.number()
        .int('Count must be an integer')
        .min(10, 'Minimum count is 10')
        .max(100, 'Maximum count is 100')
});
// Error types
export class TwitterError extends Error {
    code;
    status;
    constructor(message, code, status) {
        super(message);
        this.code = code;
        this.status = status;
        this.name = 'TwitterError';
    }
    static isRateLimit(error) {
        return error instanceof TwitterError && error.code === 'rate_limit_exceeded';
    }
}
