export class ResponseFormatter {
    static formatTweet(tweet, user, position) {
        return {
            position,
            author: {
                username: user.username
            },
            content: tweet.text,
            metrics: tweet.metrics,
            url: `https://twitter.com/${user.username}/status/${tweet.id}`
        };
    }
    static formatSearchResponse(query, tweets, users) {
        const userMap = new Map(users.map(user => [user.id, user]));
        const formattedTweets = tweets
            .map((tweet, index) => {
            const user = userMap.get(tweet.authorId);
            if (!user)
                return null;
            return this.formatTweet(tweet, user, index + 1);
        })
            .filter((tweet) => tweet !== null);
        return {
            query,
            count: formattedTweets.length,
            tweets: formattedTweets
        };
    }
    static toMcpResponse(response) {
        const header = [
            'TWITTER SEARCH RESULTS',
            `Query: "${response.query}"`,
            `Found ${response.count} tweets`,
            '='
        ].join('\n');
        if (response.count === 0) {
            return header + '\nNo tweets found matching your query.';
        }
        const tweetBlocks = response.tweets.map(tweet => [
            `Tweet #${tweet.position}`,
            `From: @${tweet.author.username}`,
            `Content: ${tweet.content}`,
            `Metrics: ${tweet.metrics.likes} likes, ${tweet.metrics.retweets} retweets`,
            `URL: ${tweet.url}`,
            '='
        ].join('\n'));
        return [header, ...tweetBlocks].join('\n\n');
    }
}
