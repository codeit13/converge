<template>
  <div class="h-[90vh] w-full flex flex-col overflow-hidden">
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
              <CardTitle class="font-display text-lg md:text-xl">Chat with AI</CardTitle>
              <CardDescription class="text-xs md:text-sm">
                Ask questions or give instructions
              </CardDescription>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <Button variant="ghost" size="sm" class="text-xs md:text-sm" @click="clearChat">
              <RefreshCw class="h-3.5 w-3.5 mr-1" />
              New Chat
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent
        class="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar"
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
            class="flex items-start gap-2 ml-auto max-w-[85%] md:max-w-[75%] lg:max-w-[70%] px-1"
          >
            <div
              class="rounded-2xl bg-primary text-primary-foreground p-3 shadow-sm break-words w-full"
            >
              <p class="font-medium text-sm md:text-base">{{ message.content }}</p>
            </div>
            <Avatar class="h-8 w-8 shrink-0">
              <AvatarImage src="" />
              <AvatarFallback class="bg-primary text-primary-foreground">
                <User class="h-4 w-4" />
              </AvatarFallback>
            </Avatar>
          </div>

          <!-- Thinking indicator for tool calls and processing -->
          <div
            v-if="message.thinkingMessage"
            class="animate-pulse thinking-indicator ml-10 md:ml-12 mb-2 max-w-[80%]"
          >
            <div class="thinking-indicator-icon">
              <Lightbulb class="h-3.5 w-3.5" />
            </div>
            <div class="thinking-indicator-content">
              <span class="text-xs md:text-sm">{{ message.thinkingMessage }}</span>
              <div class="typing-animation">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
              </div>
            </div>
          </div>

          <!-- AI message -->
          <div
            v-else-if="message.role === 'assistant'"
            v-motion="{
              initial: { opacity: 0, x: -20 },
              enter: { opacity: 1, x: 0, transition: { duration: 300 } },
            }"
            class="group flex items-start gap-2 max-w-[85%] md:max-w-[75%] lg:max-w-[70%] px-1"
          >
            <Avatar class="h-8 w-8 shrink-0">
              <AvatarImage src="" />
              <AvatarFallback class="bg-secondary text-secondary-foreground">
                <Bot class="h-4 w-4" />
              </AvatarFallback>
            </Avatar>
            <div
              class="relative rounded-2xl bg-muted/50 p-3 shadow-sm break-words w-full"
              :class="{
                'animate-pulse':
                  isLoading && message === messages[messages.length - 1],
              }"
            >
              <div
                v-if="message.content"
                v-html="formatMessage(message.content)"
                class="prose prose-sm max-w-none dark:prose-invert"
              ></div>
              <div v-else class="flex items-center space-x-2">
                <div class="animate-pulse font-medium">Thinking</div>
                <div class="flex space-x-1">
                  <span
                    class="animate-bounce delay-0 h-1.5 w-1.5 rounded-full bg-muted-foreground"
                  ></span>
                  <span
                    class="animate-bounce delay-150 h-1.5 w-1.5 rounded-full bg-muted-foreground"
                  ></span>
                  <span
                    class="animate-bounce delay-300 h-1.5 w-1.5 rounded-full bg-muted-foreground"
                  ></span>
                </div>
              </div>

              <!-- Message actions on hover -->
              <div
                class="absolute -top-3 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex space-x-1 bg-background rounded-md shadow-sm border p-1"
              >
                <Button
                  variant="ghost"
                  size="icon"
                  @click="copyToClipboard(message.content)"
                  class="h-7 w-7"
                  title="Copy message"
                >
                  <Copy class="h-3.5 w-3.5" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  @click="regenerateResponse(message)"
                  class="h-7 w-7"
                  title="Regenerate response"
                >
                  <RefreshCw class="h-3.5 w-3.5" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  @click="saveToNotes(message)"
                  class="h-7 w-7"
                  title="Save to notes"
                >
                  <Save class="h-3.5 w-3.5" />
                </Button>
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
      <div class="p-4 md:p-5 lg:p-6 border-t">
        <!-- Response type toggle and options -->
        <div class="flex items-center justify-between mb-3 px-1">
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
            <Button 
              variant="outline" 
              size="sm" 
              class="text-xs h-7 px-2"
            >
              <Copy class="h-3 w-3 mr-1" />
              Copy
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
        </div>
        
        <form @submit.prevent="sendMessage" class="flex space-x-2 md:space-x-3">
          <div class="relative flex-1 items-center justify-center">
            <Input
              type="text"
              v-model="userInput"
              placeholder="Type your message..."
              class="min-h-10 md:min-h-12 pr-10 rounded-xl border-muted-foreground/20 focus:border-primary focus:ring-primary shadow-sm font-medium text-sm md:text-base"
              @keydown.enter.prevent="handleEnterKey"
              @input="adjustTextareaHeight"
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

    <!-- Toast notifications are handled by global store -->
  </div>
</template>

<!-- Component imports using script setup -->
<script setup>
// Component imports only
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Bot,
  Copy,
  Lightbulb,
  RefreshCw,
  Save,
  Send,
  User,
  X,
} from "lucide-vue-next";
</script>

<script>
import { mapState } from "vuex";
import DOMPurify from "dompurify";
import { marked } from "marked";
import { useMotion } from "@vueuse/motion";
import Input from "@/components/ui/input/Input.vue";

export default {
  // 3. Props definition
  props: {},

  // 4. Component data
  data() {
    return {
      userInput: "",
      messages: [],
      isLoading: false,
      lastUserMessage: "",
      useStreaming: true, // Default to streaming responses
    };
  },

  // 5. Computed properties
  computed: {
    latestAiMessage() {
      // Find the most recent AI message
      for (let i = this.messages.length - 1; i >= 0; i--) {
        if (this.messages[i].role === "assistant" && this.messages[i].content) {
          return this.messages[i];
        }
      }
      return null;
    },
  },

  // 6. Watchers
  watch: {
    messages: {
      deep: true,
      handler() {
        console.log("Messages changed:", this.messages);
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      },
    },
  },

  // 7. Lifecycle hooks
  created() {
    // Add a welcome system message
    this.messages.push({
      role: "system",
      content: "Conversation started",
    });
  },

  mounted() {
    this.$store.commit("SET_SIDEBAR_OPEN", false);

    // Focus the input field when component is mounted
    this.$nextTick(() => {
      if (
        this.$refs.messageInput &&
        typeof this.$refs.messageInput.focus === "function"
      ) {
        this.$refs.messageInput.focus();
      }
    });
  },

  unmounted() {
    // No cleanup needed
    this.$store.commit("SET_SIDEBAR_OPEN", true);
  },

  // 8. Methods
  methods: {
    clearChat() {
      this.messages = [];
      this.userInput = "";
      this.isLoading = false;
      this.streamingResponse = "";
      
      // Add a welcome system message
      this.messages.push({
        role: "system",
        content: "Conversation started",
      });
    },
    
    copyConversation() {
      // Format the conversation for copying
      const formattedConversation = this.messages
        .filter(message => message.role !== "system")
        .map(message => {
          const role = message.role === 'user' ? 'User' : 'AI';
          return `${role}: ${message.content}`;
        }).join('\n\n');
      
      // Use existing copyToClipboard method
      this.copyToClipboard(formattedConversation);
    },
    async sendMessage() {
      const userMessage = this.userInput.trim();
      if (!userMessage || this.isLoading) return;

      // Add user message to chat
      this.messages.push({
        role: "user",
        content: userMessage,
      });

      // Scroll to bottom immediately after adding user message
      this.scrollToBottom();

      // Clear input and save last message
      this.lastUserMessage = userMessage;
      this.userInput = "";
      this.adjustTextareaHeight();

      // Add placeholder for AI response
      this.messages.push({
        role: "assistant",
        content: "",
        thinkingMessage: null,
      });

      // Set loading state
      this.isLoading = true;

      // Get the index of the AI message we'll be updating
      const aiMessageIndex = this.messages.length - 1;

      if (this.useStreaming) {
        // Use streaming API
        let fullResponse = "";
        let currentThinking = "";

        // Start the streaming connection
        const stream = this.$store.dispatch("streamAgent", {
          userPrompt: userMessage,
          onMessage: (data) => {
            // Handle raw chunks from the backend
            if (data.type === "chunk" && data.data) {
              const chunk = data.data;

              // Process based on chunk content
              if (
                chunk.agent &&
                chunk.agent.messages &&
                chunk.agent.messages.length > 0
              ) {
                // Extract the actual message content from the agent response
                const message = chunk.agent.messages[0];
                if (message.content) {
                  // This is the final answer
                  fullResponse = message.content;
                  this.messages[aiMessageIndex].content = fullResponse;
                  this.scrollToBottom();
                }
              } else if (chunk.output) {
                // Direct output from the agent
                fullResponse = chunk.output;
                this.messages[aiMessageIndex].content = fullResponse;
                this.scrollToBottom();
              } else if (chunk.actions && chunk.actions.length > 0) {
                // Agent is thinking or taking an action
                const action = chunk.actions[0];
                const toolName = action.tool || "unknown tool";
                const toolInput = action.tool_input || "unknown input";

                currentThinking = `Using ${toolName} with input: ${toolInput}`;
                this.messages[aiMessageIndex].content =
                  fullResponse +
                  (fullResponse ? "\n\n" : "") +
                  "*" +
                  currentThinking +
                  "*";
                this.scrollToBottom();
              } else if (chunk.steps && chunk.steps.length > 0) {
                // Results from tool execution
                for (const step of chunk.steps) {
                  if (step.observation) {
                    const observation = step.observation.toString();
                    currentThinking += "\n→ " + observation;
                    this.messages[aiMessageIndex].content =
                      fullResponse +
                      (fullResponse ? "\n\n" : "") +
                      "*" +
                      currentThinking +
                      "*";
                    this.scrollToBottom();
                  }
                }
              }
            } else if (data.type === "thinking") {
              // Handle thinking message from the backend
              // Instead of adding to content, set the thinkingMessage property
              this.messages[aiMessageIndex].thinkingMessage = data.content;
              this.scrollToBottom();
            } else if (data.type === "observation") {
              // Legacy observation message format
              currentThinking += "\n→ " + data.content;
              this.messages[aiMessageIndex].content =
                fullResponse +
                (fullResponse ? "\n\n" : "") +
                "*" +
                currentThinking +
                "*";
              this.scrollToBottom();
            } else if (data.type === "answer") {
              // Legacy answer message format
              fullResponse = data.content;
              this.messages[aiMessageIndex].content = fullResponse;
              this.scrollToBottom();
            } else if (data.type === "error") {
              // Error message from the backend
              this.messages[aiMessageIndex].content = "Error: " + data.content;
              this.scrollToBottom();
            } else if (data.type === "info") {
              // Info message - don't update UI
            }
          },
          onError: (error) => {
            console.error("Streaming error:", error);
            // Update with error message if the stream fails
            this.messages[aiMessageIndex].content =
              "Sorry, I encountered an error while processing your request.";

            // Add system message about the error
            this.messages.push({
              role: "system",
              content:
                "An error occurred with the streaming connection. Please try again.",
            });
            this.isLoading = false;
          },
          onComplete: () => {
            // Streaming completed
            this.isLoading = false;

            // Clear any thinking messages when streaming is complete
            if (this.messages[aiMessageIndex]) {
              this.messages[aiMessageIndex].thinkingMessage = null;
            }
          },
        });

        // Set up a timeout to close the stream if it takes too long
        setTimeout(() => {
          if (this.isLoading) {
            stream.close();
            this.isLoading = false;
          }
        }, 60000); // 1 minute timeout
      } else {
        // Use regular API
        try {
          // Call the runAgent action from Vuex store
          const response = await this.$store.dispatch("runAgent", userMessage);

          // Update the AI message with the response
          this.messages[aiMessageIndex].content =
            response.data?.response || "I processed your request.";
        } catch (error) {
          console.error("Error running agent:", error);

          // Update with error message
          this.messages[aiMessageIndex].content =
            "Sorry, I encountered an error processing your request.";

          // Add system message about the error
          this.messages.push({
            role: "system",
            content: "An error occurred. Please try again.",
          });
        } finally {
          this.isLoading = false;
        }
      }
    },

    handleEnterKey(e) {
      // Send message on Enter, but allow Shift+Enter for new lines
      if (!e.shiftKey && this.userInput.trim()) {
        this.sendMessage();
      } else if (e.shiftKey) {
        // Allow default behavior for Shift+Enter (new line)
        const textarea = this.$refs.messageInput;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        this.userInput =
          this.userInput.substring(0, start) +
          "\n" +
          this.userInput.substring(end);
        this.$nextTick(() => {
          textarea.selectionStart = textarea.selectionEnd = start + 1;
          this.adjustTextareaHeight();
        });
      }
    },

    adjustTextareaHeight() {
      this.$nextTick(() => {
        const textarea = this.$refs.messageInput;
        if (!textarea || !textarea.style) return;

        try {
          // Reset height to calculate properly
          textarea.style.height = "auto";

          // Set new height based on scrollHeight, with a max height
          const newHeight = Math.min(textarea.scrollHeight, 150);
          textarea.style.height = `${newHeight}px`;

          // Adjust rows for the component
          this.textareaRows = Math.max(
            1,
            Math.min(5, Math.floor(newHeight / 24))
          );
        } catch (error) {
          console.error("Error adjusting textarea height:", error);
        }
      });
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatContainer;
        if (container) {
          // Use standard scrollTop property which is widely supported
          container.scrollTop = container.scrollHeight;

          // Add a second scroll check after a short delay to handle any rendering delays
          setTimeout(() => {
            if (
              container.scrollTop + container.clientHeight <
              container.scrollHeight
            ) {
              container.scrollTop = container.scrollHeight;
            }
          }, 100);
        }
      });
    },

    formatMessage(content) {
      // Convert markdown to HTML and sanitize
      if (!content) return "";
      const html = marked(content);
      return DOMPurify.sanitize(html);
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
          console.error("Failed to copy text: ", err);
          this.$store.commit("SET_TOASTER_DATA", {
            message: "Failed to copy text",
            type: "error",
            show: true,
          });
        });
    },

    regenerateResponse(message) {
      if (this.isLoading) return;

      // If a specific message is provided, use its index
      if (message) {
        const index = this.messages.indexOf(message);
        if (index !== -1 && index > 0) {
          // Find the preceding user message
          for (let i = index - 1; i >= 0; i--) {
            if (this.messages[i].role === "user") {
              // Remove the AI message
              this.messages.splice(index, 1);
              // Set user input to the found user message
              this.userInput = this.messages[i].content;
              this.sendMessage();
              return;
            }
          }
        }
      }

      // Fallback to using the last user message
      if (this.lastUserMessage) {
        // Remove the last AI message
        if (this.latestAiMessage) {
          const index = this.messages.indexOf(this.latestAiMessage);
          if (index !== -1) {
            this.messages.splice(index, 1);
          }
        }

        // Set user input to last message and send again
        this.userInput = this.lastUserMessage;
        this.sendMessage();
      }
    },

    saveToNotes(message) {
      const content = message?.content || this.latestAiMessage?.content;
      if (!content) return;

      // Show confirmation toast
      this.$store.commit("SET_TOASTER_DATA", {
        message: "Response saved to notes",
        type: "success",
        show: true,
      });

      // Here you would implement the actual save functionality
      // For example, dispatch a Vuex action to save to notes
      // this.$store.dispatch('saveToNotes', content);
    },

    // Toggle between streaming and regular responses
    toggleResponseType() {
      this.useStreaming = !this.useStreaming;

      // Show a toast notification to confirm the change
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
/* Thinking indicator for tool calls and processing */
.thinking-indicator {
  position: relative;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  background-color: rgba(0, 0, 0, 0.05);
  max-width: fit-content;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.thinking-indicator-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.thinking-indicator-icon {
  opacity: 0.8;
}

/* Typing animation dots */
.typing-animation {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.typing-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.3);
  animation: typing-animation 1.4s infinite ease-in-out both;
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

@keyframes typing-animation {
  0%,
  80%,
  100% {
    transform: scale(0.6);
    opacity: 0.6;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Animation delays for the bouncing dots */
.delay-0 {
  animation-delay: 0ms;
}

.delay-150 {
  animation-delay: 150ms;
}

.delay-300 {
  animation-delay: 300ms;
}

/* Custom scrollbar styling */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  border: none;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}

/* Dark mode scrollbar */
:deep(.dark) .custom-scrollbar {
  scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
}

:deep(.dark) .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
}

:deep(.dark) .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* Font styles */
:deep(.font-display) {
  font-family: "Inter", system-ui, sans-serif;
  letter-spacing: -0.025em;
}

/* Style for code blocks in messages */
:deep(pre) {
  background-color: hsl(var(--code));
  border-radius: 0.75rem;
  padding: 1rem;
  margin: 1rem 0;
  overflow-x: auto;
  position: relative;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

:deep(pre code) {
  font-family: "JetBrains Mono", monospace;
  font-size: 0.9rem;
  line-height: 1.5;
}

:deep(p) {
  margin-bottom: 0.75rem;
  line-height: 1.6;
}

:deep(p:last-child) {
  margin-bottom: 0;
}

:deep(h1),
:deep(h2),
:deep(h3),
:deep(h4) {
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

:deep(ul),
:deep(ol) {
  margin-left: 1.5rem;
  margin-bottom: 0.75rem;
}

:deep(li) {
  margin-bottom: 0.25rem;
}

:deep(a) {
  color: hsl(var(--primary));
  text-decoration: underline;
  text-underline-offset: 2px;
}

:deep(blockquote) {
  border-left: 3px solid hsl(var(--primary));
  padding-left: 1rem;
  color: hsl(var(--muted-foreground));
  font-style: italic;
  margin: 1rem 0;
}

:deep(hr) {
  border: none;
  border-top: 1px solid hsl(var(--border));
  margin: 1.5rem 0;
}

:deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

:deep(th),
:deep(td) {
  border: 1px solid hsl(var(--border));
  padding: 0.5rem;
  text-align: left;
}

:deep(th) {
  background-color: hsl(var(--muted));
  font-weight: 600;
}
</style>
