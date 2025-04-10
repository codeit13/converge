<template>
  <Accordion
    :collapsible="true"
    type="single"
    :default-value="isMobile ? 'chat-history' : undefined"
    class="pb-4 w-[80vw] md:w-full lg:w-full"
  >
    <AccordionItem value="chat-history">
      <AccordionTrigger
        class="flex flex-row gap-y-1.5 mt-6 ml-6 md:mt-3 md:ml-0 hover:bg-none p-6 py-3 md:py-4 px-0 md:px-6 border-none md:hover:bg-secondary/5 rounded-lg text-sm font-medium"
      >
        <div class="flex w-fit md:w-full items-center gap-2">
          <Clock class="h-4 w-4 text-muted-foreground" />
          <div>
            Chat History <span class="ml-1.5">({{ chatSessions.length }})</span>
          </div>
        </div>
      </AccordionTrigger>
      <AccordionContent class="mt-2 md:mt-4 space-y-4">
        <slot></slot>
      </AccordionContent>
    </AccordionItem>
  </Accordion>
</template>

<script setup>
import { Clock } from "lucide-vue-next";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion";

defineProps({
  chatSessions: {
    type: Array,
    required: true,
  },
  isMobile: {
    type: Boolean,
    default: false,
  },
});
</script>
