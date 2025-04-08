<template>
  <div
    class="h-[90vh] w-full flex flex-col overflow-hidden"
    :style="{
      fontFamily: `ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'`,
    }"
  >
    <Card
      class="flex-1 flex flex-col overflow-hidden shadow-lg border-none m-0 rounded-none bg-gradient-to-l from-background via-secondary/5 to-background"
    >
      <CardHeader class="border-b py-3 md:py-4 px-4 md:px-6">
        <div
          v-motion="{
            initial: { opacity: 0, y: -20 },
            enter: { opacity: 1, y: 0, transition: { duration: 500 } },
          }"
          class="flex items-center justify-between w-full"
        >
          <div class="flex items-center gap-2">
            <Bot class="h-5 w-5 md:h-6 md:w-6 text-primary" />
            <div>
              <CardTitle class="font-display text-lg md:text-xl">
                Chat with AI
              </CardTitle>
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            class="text-xs md:text-sm"
            @click="clearChat"
          >
            <RefreshCw class="h-3 w-3 mr-1" />
            New Chat
          </Button>
        </div>
      </CardHeader>

      <CardContent
        class="flex-1 overflow-y-auto px-0 py-6 md:p-6 space-y-6 custom-scrollbar"
        id="chat-container"
        ref="chatContainer"
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
          class="flex flex-col items-center justify-center h-full text-center space-y-6 text-muted-foreground"
        >
          <div class="rounded-full bg-primary/10 p-6">
            <Bot class="h-12 w-12 text-primary" />
          </div>
          <div>
            <h3 class="text-xl font-display font-medium mb-2">
              Start a conversation
            </h3>
            <p class="text-muted-foreground">
              Ask a question or give an instruction to begin
            </p>
          </div>
        </div>

        <!-- Chat messages -->
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
            class="flex items-start gap-2 rounded-lg ml-auto max-w-[85%] md:max-w-[75%] lg:max-w-[70%] px-1"
          >
            <div class="rounded-2xl p-3 shadow-sm break-words w-full">
              <p class="font-medium text-sm md:text-base text-[#b3b3b3]">
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
            class="flex items-start gap-2 max-w-[95%] md:max-w-[75%] lg:max-w-[70%] px-1"
          >
            <Avatar class="h-8 w-8 shrink-0">
              <AvatarImage src="" />
              <AvatarFallback class="bg-secondary text-secondary-foreground">
                <Bot class="h-4 w-4" />
              </AvatarFallback>
            </Avatar>
            <div class="flex flex-col w-full space-y-3">
              <!-- Thinking section - collapsible -->
              <div
                v-if="message.thinking && message.thinking.length > 0"
                class="w-full"
              >
                <div
                  class="flex items-center gap-2 px-3 py-1.5 cursor-pointer transition-colors rounded-lg hover:bg-secondary/5"
                  @click="toggleThinking(message)"
                >
                  <span class="text-normal font-medium text-muted-foreground">
                    {{
                      message?.thinkingTime
                        ? "Thought for"
                        : "Reasoning & Tools"
                    }}
                    <span
                      v-if="message.thinkingTime"
                      class="ml-2 text-xs text-muted-foreground/70"
                    >
                      ({{ formatTime(message.thinkingTime) }})
                    </span>
                  </span>
                  <ChevronDown
                    class="h-3.5 w-3.5 ml-auto transition-transform text-muted-foreground"
                    :class="{ 'rotate-180': message.showThinking }"
                  />
                </div>
                <div
                  class="relative rounded-lg px-3 py-0 mt-2 text-sm bg-background/5 transition-all duration-2000 h-full overflow-hidden"
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
                class="group relative rounded-lg px-2 py-1 md:py-2 md:px-4 break-words w-full backdrop-blur-sm"
                :class="{
                  'bg-secondary/0': message.role === 'assistant',
                  'bg-secondary': message.role === 'user',
                }"
              >
                <div
                  v-if="message.content"
                  v-html="formatMessage(message)"
                  class="prose prose-sm max-w-none dark:prose-invert text-[#b3b3b3] tracking-wide"
                ></div>
                <div
                  v-else
                  class="animate-bounce flex items-center space-x-2 pt-2 pb-3 md:pt-0"
                >
                  <span
                    class="font-medium tracking-wide text-sm text-muted-foreground"
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
      <div class="p-2 md:p-5 lg:p-6">
        <!-- Response type toggle and options -->
        <!--<div class="flex items-center justify-between mb-3 px-1">
          
          <div class="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              class="text-xs h-7 px-2"
              @click="clearChat"
            >
              <RefreshCw class="h-3 w-3 mr-1" />
              New Chat
            </Button>
          </div>
          
          <div class="flex items-center space-x-2">
            <span class="text-xs text-muted-foreground">Regular</span>
            <button
              @click="toggleResponseType"
              type="button"
              class="relative inline-flex h-5 w-10 items-center rounded-full transition-colors"
              :class="useStreaming ? 'bg-secondary' : 'bg-muted'"
            >
              <span
                class="inline-block h-3.5 w-3.5 transform rounded-full bg-white transition-transform"
                :class="useStreaming ? 'translate-x-5.5' : 'translate-x-1'"
              />
            </button>
            <span class="text-xs text-muted-foreground">Streaming</span>
          </div>
        </div> -->

        <form @submit.prevent="sendMessage" class="flex space-x-2 md:space-x-3">
          <div class="relative flex-1 items-center justify-center">
            <Input
              type="text"
              v-model="userInput"
              placeholder="Type your message..."
              class="min-h-10 md:min-h-12 pr-10 rounded-xl border-muted-foreground/20 focus:border-primary focus:ring-primary shadow-sm font-medium text-sm md:text-base"
              @keydown.enter.prevent="handleEnterKey"
              ref="messageInput"
            />
            <Button
              v-if="userInput.trim().length > 0"
              type="button"
              variant="ghost"
              size="icon"
              class="absolute right-3 top-1/2 transform -translate-y-1/2 opacity-70 hover:opacity-100 transition-opacity h-6 w-6"
              @click="userInput = ''"
            >
              <X class="h-3.5 w-3.5" />
            </Button>
          </div>
          <Button
            type="submit"
            :disabled="isLoading || userInput.trim().length === 0"
            class="rounded-xl h-10 w-10 md:h-12 md:w-12 p-0 bg-primary hover:bg-primary/90 transition-colors shadow-md flex-shrink-0"
            v-motion:hover="{
              scale: 1.05,
              transition: { type: 'spring', stiffness: 300, damping: 15 },
            }"
          >
            <Send class="h-4 w-4 md:h-5 md:w-5" />
          </Button>
        </form>
      </div>
    </Card>
  </div>
</template>

<script>
// Component imports
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import Input from "@/components/ui/input/Input.vue";
import {
  Bot,
  ChevronDown,
  Copy,
  Lightbulb,
  RefreshCw,
  Save,
  Send,
  User,
  X,
} from "lucide-vue-next";
import DOMPurify from "dompurify";
import { marked } from "marked";

export default {
  name: "Chat",
  components: {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Button,
    Avatar,
    AvatarFallback,
    AvatarImage,
    Input,
    Bot,
    ChevronDown,
    Copy,
    Lightbulb,
    RefreshCw,
    Save,
    Send,
    User,
    X,
  },
  data() {
    return {
      userInput: "",
      messages: [
        {
          role: "system",
          content: "Conversation started",
        },
      ],
      isLoading: false,
      lastUserMessage: "",
      useStreaming: true,
    };
  },
  computed: {
    latestAiMessage() {
      for (let i = this.messages.length - 1; i >= 0; i--) {
        if (this.messages[i].role === "assistant" && this.messages[i].content) {
          return this.messages[i];
        }
      }
      return null;
    },
  },
  watch: {
    messages: {
      deep: true,
      handler() {
        this.scrollToBottom();
      },
    },
  },
  mounted() {
    this.$store.commit("SET_SIDEBAR_OPEN", false);
    const inputComponent = this.$refs.messageInput;
    if (inputComponent && inputComponent.$el) {
      const inputElement = inputComponent.$el.querySelector("input");
      if (inputElement) {
        inputElement.focus();
      }
    }
  },
  unmounted() {
    this.$store.commit("SET_SIDEBAR_OPEN", true);
  },
  methods: {
    openLink(link) {
      window.open(link, "_blank");
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
      const messageText = this.userInput.trim();
      if (!messageText || this.isLoading) return;

      // Add user message
      this.messages.push({
        role: "user",
        content: messageText,
      });

      // Scroll to bottom immediately
      this.scrollToBottom();

      // Clear input and save last message
      this.lastUserMessage = messageText;
      this.userInput = "";

      // Add placeholder for AI response
      const aiMessage = {
        role: "assistant",
        content: "",
        thinking: [],
        showThinking: true, // Start with thinking expanded
        thinkingStartTime: Date.now(), // Start tracking time
      };
      this.messages.push(aiMessage);

      // Set loading state
      this.isLoading = true;
      const aiMessageIndex = this.messages.length - 1;

      if (this.useStreaming) {
        // Use streaming API
        let fullResponse = "";

        const stream = this.$store.dispatch("streamAgent", {
          userPrompt: messageText,
          onMessage: (data) => {
            console.log("Stream data:", data);
            // Process each stream message based on type

            if (data.type === "thinking") {
              // Add thinking step
              this.messages[aiMessageIndex].thinking.push({
                type: "thinking",
                data: data.data,
              });
              this.scrollToBottom();
            } else if (data.type == "tool_calls") {
              const tools = data?.data || [];

              this.messages[aiMessageIndex].thinking.push({
                type: "tool_calls",
                data: tools,
              });
              this.scrollToBottom();
            } else if (data.type == "tool_messages") {
              const message =
                data?.data?.messages[data?.data?.messages.length - 1];

              if (message) {
                let messageContent = message?.content;
                try {
                  if (typeof messageContent == "object") {
                    messageContent = JSON.stringify(messageContent, null, 2);
                  } else {
                    messageContent = JSON.parse(messageContent);
                    messageContent = JSON.stringify(messageContent, null, 2);
                  }
                } catch (e) {
                  console.log(e);
                }
                this.messages[aiMessageIndex].thinking.push({
                  type: "tool_messages",
                  data: messageContent,
                });
              }
              this.scrollToBottom();
            } else if (data.type === "chunk" && data.data && data.data != "") {
              let chunk = data.data;

              console.log("chunk: ", chunk);
              try {
                chunk = JSON.parse(chunk);
              } catch (e) {
                console.log(
                  "Seems like chunk is already a valid string, processing it"
                );
              }

              // Handle direct message chunks
              if (typeof chunk == "object" && chunk.message_to_user) {
                fullResponse = chunk.message_to_user;
                this.messages[aiMessageIndex].content = fullResponse;
              } else {
                fullResponse = chunk;
                this.messages[aiMessageIndex].content = chunk;
              }

              this.scrollToBottom();
            } else if (data.type == "complete") {
              const article = data?.data?.article;
              if (article && article?.link) {
                this.messages[aiMessageIndex].content +=
                  "\n\n\n Article is now live at [" + article.link + "](Link)";
              }
            } else if (data.type == "error") {
              this.messages[
                aiMessageIndex
              ].content = `Seems like our servers are taking a coffee break. Please try again after the break :)\n\n${data.data}`;

              this.isLoading = false;
              this.scrollToBottom();
            }
          },
          onError: (error) => {
            console.error("Streaming error:", error);
            this.messages[
              aiMessageIndex
            ].content = `Seems like our servers are taking a coffee break. Please try again after the break :)\n\n${error}`;
            this.isLoading = false;
            this.scrollToBottom();
          },
          onComplete: () => {
            this.isLoading = false;
            if (this.messages[aiMessageIndex]) {
              // Calculate thinking time
              const endTime = Date.now();
              const thinkingTime = Math.round(
                (endTime - aiMessage.thinkingStartTime) / 1000
              );
              this.messages[aiMessageIndex].thinkingTime = thinkingTime;

              // Auto collapse thinking when complete
              setTimeout(() => {
                if (this.messages[aiMessageIndex]) {
                  this.messages[aiMessageIndex].showThinking = false;
                }
              }, 1000);
            }
            this.scrollToBottom();
          },
        });

        // Set timeout for stream
        // setTimeout(() => {
        //   if (this.isLoading) {
        //     stream.close();
        //     this.isLoading = false;
        //   }
        // }, 60000);
      } else {
        // Use regular API
        try {
          const response = await this.$store.dispatch("runAgent", messageText);
          this.messages[aiMessageIndex].content =
            response.data?.response || "I processed your request.";
        } catch (error) {
          console.error("Error running agent:", error);
          this.messages[aiMessageIndex].content =
            "Sorry, I encountered an error processing your request.";
          this.messages.push({
            role: "system",
            content: "An error occurred. Please try again.",
          });
        } finally {
          this.isLoading = false;
          this.scrollToBottom();
        }
      }
    },
    handleEnterKey(e) {
      if (!e.shiftKey && this.userInput.trim()) {
        this.sendMessage();
      } else if (e.shiftKey) {
        // Allow Shift+Enter for new line
        const input = this.$refs.messageInput.$el.querySelector("input");

        const start = input.selectionStart;
        const end = input.selectionEnd;
        this.userInput =
          this.userInput.substring(0, start) +
          "\n" +
          this.userInput.substring(end);
        input.selectionStart = input.selectionEnd = start + 1;
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
    },
    formatMessage(message) {
      let content = message?.content ?? "";
      if (!content) return "";

      const html = marked.parse(content);
      return DOMPurify.sanitize(html);
    },
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes}min ${remainingSeconds}s`;
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
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.1);
}

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
