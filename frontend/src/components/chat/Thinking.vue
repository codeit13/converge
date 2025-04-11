<template>
  <Accordion :collapsible="true" class="border-0">
    <AccordionItem :value="`thinking-${messageId || index}`" class="border-0">
      <AccordionTrigger
        class="flex items-center gap-2 px-3 py-1.5 transition-colors rounded-lg hover:bg-secondary/5 no-underline"
      >
        <span class="text-sm font-medium text-muted-foreground/70">
          {{ thinkingTime ? "Thought for" : "Reasoning & Tools" }}
          <span
            v-if="thinkingTime"
            class="ml-0.5 font-medium text-muted-foreground/80"
          >
            {{ formatTime(thinkingTime) }}
          </span>
        </span>
        <template #icon>
          <ChevronDown
            class="h-3.5 w-3.5 ml-auto transition-transform text-muted-foreground"
          />
        </template>
      </AccordionTrigger>
      <AccordionContent class="px-3 py-0 mt-1 text-sm bg-background/5">
        <div class="relative">
          <div
            class="bg-primary/10 absolute top-1 left-0 w-1 h-full rounded-full"
          ></div>
          <div
            v-for="(step, i) in thinking"
            :key="`thinking-${i}`"
            class="mb-1 ml-2"
          >
            <div class="flex items-center gap-2">
              <div class="font-medium text-sm break-words">
                <!-- Thinking data -->
                <div v-if="step.type === 'thinking'">
                  {{ step.data }}
                </div>

                <!-- Tool calls -->
                <div
                  v-else-if="step.type === 'tool_calls'"
                  class="text-secondary"
                >
                  Calling
                  {{ step.data.join(", ") }}
                  {{ (step?.data || []).length == 1 ? "tool" : "tools" }}
                </div>

                <!-- Tool messages -->
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
                      <div v-if="typeof value === 'object' && value !== null">
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
      </AccordionContent>
    </AccordionItem>
  </Accordion>
</template>

<script setup>
import { ChevronDown } from "lucide-vue-next";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion";

defineProps({
  thinking: {
    type: Array,
    required: true,
    default: () => [],
  },
  messageId: {
    type: String,
    default: "",
  },
  index: {
    type: Number,
    default: 0,
  },
  thinkingTime: {
    type: Number,
    default: 0,
  },
  availableTools: {
    type: Object,
    default: () => ({}),
  },
});

// Format time (seconds) to a readable format
const formatTime = (seconds) => {
  if (seconds < 60) {
    return `${seconds.toFixed(1)}s`;
  } else if (seconds < 3600) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}m ${secs}s`;
  } else {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  }
};
</script>
