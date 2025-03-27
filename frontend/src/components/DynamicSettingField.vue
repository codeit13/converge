<template>
  <div
    class="setting-field-wrapper mb-6 relative"
    :class="{
      'w-full md:w-[50%] ml-0 md:ml-1': parent,
      'border-l-2 border-primary/10 pl-4 py-2': isNested,
    }"
  >
    <div
      class="flex w-full"
      :class="{
        'flex-row gap-4 items-center justify-between': !(
          config?.type == 'object'
        ),
        'flex-col gap-0.5': config?.type == 'object',
      }"
    >
      <!-- Label with optional tooltip -->
      <div
        class="flex items-center gap-3"
        :class="{
          'min-w-[180px]': !(config?.type == 'object'),
          'w-full mb-2': config?.type == 'object',
        }"
      >
        <Label class="block capitalize text-sm font-medium" :for="fieldId">
          {{ formatLabel(config.label || "") }}
        </Label>
        <TooltipProvider v-if="config?.description">
          <Tooltip>
            <TooltipTrigger>
              <Info class="h-4 w-4 text-muted-foreground" />
            </TooltipTrigger>
            <TooltipContent>
              <p>{{ config?.description }}</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      </div>

      <!-- Field wrapper with validation -->
      <div
        class="flex-1 space-y-2"
        :class="{
          'w-fit min-w-[140px]': !(config?.type == 'object'),
          'w-full': config?.type == 'object',
        }"
      >
        <!-- Boolean field -->
        <div
          v-if="config?.type === 'boolean'"
          class="flex items-center gap-3"
          :class="{ 'justify-between': parent }"
        >
          <Switch
            :id="fieldId"
            v-model="internalValue"
            :disabled="config?.disabled"
            class="data-[state=checked]:bg-primary"
          />
          <!-- <span class="text-sm text-muted-foreground">
            {{ internalValue ? "✓" : "✗" }}
          </span> -->
        </div>

        <!-- Number field -->
        <div v-else-if="config?.type === 'number'" class="relative space-y-1.5">
          <Input
            :id="fieldId"
            type="number"
            v-model.number="internalValue"
            :min="config?.validations?.min"
            :max="config?.validations?.max"
            :step="config?.step || 1"
            :disabled="config?.disabled"
            :placeholder="config?.placeholder"
            class="w-full"
            :class="{ 'border-destructive': hasError }"
          />
          <span v-if="hasError" class="text-xs text-destructive block">
            {{ validationError }}
          </span>
        </div>

        <!-- Object field (nested) -->
        <div
          v-else-if="config?.type === 'object'"
          class="w-full space-y-4 mt-2 rounded-lg border border-border/50 p-4"
        >
          <template v-for="(fieldConfig, key) in config.fields" :key="key">
            <DynamicSettingField
              v-if="fieldConfig.active !== false"
              :id="`${fieldId}-${key}`"
              :modelValue="modelValue?.[key] ?? fieldConfig.value"
              @update:modelValue="(val) => updateFieldValue(key, val)"
              :config="{
                ...fieldConfig,
                label: formatLabel(key),
                active: fieldConfig.active,
                description: fieldConfig.description,
              }"
              :parent="modelValue"
              :isNested="true"
            />
          </template>
        </div>

        <!-- String field -->
        <div
          v-else-if="config?.type === 'text' || config?.type === 'textarea'"
          class="relative space-y-1.5"
        >
          <template v-if="config?.type === 'text'">
            <Input
              :id="fieldId"
              type="text"
              v-model="internalValue"
              :disabled="config?.disabled"
              :placeholder="config?.placeholder"
              class="w-full"
              :class="{ 'border-destructive': hasError }"
            />
          </template>
          <template v-else>
            <Textarea
              :id="fieldId"
              v-model="internalValue"
              :disabled="config?.disabled"
              :placeholder="config?.placeholder"
              :rows="config?.rows || 3"
              class="w-full resize-none"
              :class="{ 'border-destructive': hasError }"
            />
          </template>
          <span v-if="hasError" class="text-xs text-destructive block">
            {{ validationError }}
          </span>
        </div>

        <!-- Select field -->
        <div
          v-else-if="config?.type === 'select'"
          class="relative w-full flex flex-col gap-2"
        >
          <Select v-model="internalValue" :disabled="config.disabled">
            <SelectTrigger
              class="w-full"
              :class="{ 'border-destructive': hasError }"
            >
              <SelectValue
                :placeholder="config.placeholder || 'Select an option'"
              />
            </SelectTrigger>
            <SelectContent class="w-full">
              <SelectGroup>
                <SelectItem
                  v-for="option in config.options"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
          <span v-if="hasError" class="text-xs text-destructive block">
            {{ validationError }}
          </span>
        </div>

        <!-- Default field (fallback) -->
        <div v-else class="relative flex items-center gap-3">
          <Input
            :id="fieldId"
            type="text"
            v-model="internalValue"
            :disabled="config.disabled"
            :placeholder="config.placeholder"
            class="w-full"
            :class="{ 'border-destructive': hasError }"
          />
          <span v-if="hasError" class="text-xs text-destructive block">
            {{ validationError }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Component imports only
import { Info } from "lucide-vue-next";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
</script>

<script>
export default {
  name: "DynamicSettingField",
  props: {
    modelValue: {
      required: true,
    },
    config: {
      type: Object,
      required: true,
      validator(value) {
        return value && typeof value === "object";
      },
    },
    parent: {
      type: Object,
      default: null,
    },
    isNested: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      validationError: "",
      nestedValidationErrors: {},
    };
  },
  computed: {
    fieldId() {
      return `setting-${this.config?.label
        ?.toLowerCase()
        .replace(/\s+/g, "-")}`;
    },

    hasError() {
      return (
        Boolean(this.validationError) ||
        Object.keys(this.nestedValidationErrors).length > 0
      );
    },

    internalValue: {
      get() {
        if (this.config?.type === "object" && this.config?.fields) {
          // For object type settings, return the entire object or empty object
          return this.modelValue ?? {};
        }
        // For simple settings, return the value or field's default
        return this.modelValue ?? this.config?.value;
      },
      set(val) {
        const validationResult = this.validateValue(
          val,
          this.config?.validations
        );
        if (validationResult === true) {
          this.validationError = "";
          if (this.config?.type === "object" && this.config?.fields) {
            // For object type settings, update only changed fields
            const updatedFields = { ...this.modelValue };
            Object.entries(val).forEach(([key, value]) => {
              if (this.config.fields[key]?.active) {
                updatedFields[key] = value;
              }
            });
            this.$emit("update:modelValue", updatedFields);
          } else {
            // For simple settings, emit the value directly
            this.$emit("update:modelValue", val);
          }
        } else {
          this.validationError = validationResult;
        }
      },
    },

    fieldValidationError() {
      if (this.config?.type === "object") {
        return Object.values(this.nestedValidationErrors)[0] || "";
      }
      return this.validationError;
    },
  },

  methods: {
    formatLabel(label) {
      return label
        .split(/(?=[A-Z])/)
        .join(" ")
        .toLowerCase()
        .replace(/^\w/, (c) => c.toUpperCase());
    },

    getNestedDescription(key) {
      return this.config.fields?.[key]?.description || "";
    },

    updateFieldValue(key, value) {
      if (this.config.type === "object" && this.config.fields) {
        const fieldConfig = this.config.fields[key];
        if (!fieldConfig?.active) return;

        const validationResult = this.validateValue(
          value,
          fieldConfig.validations
        );
        if (validationResult === true) {
          this.nestedValidationErrors[key] = "";
          // Update only the specific field value while preserving others
          const updatedFields = { ...(this.modelValue ?? {}) };
          updatedFields[key] = value;
          this.$emit("update:modelValue", updatedFields);
        } else {
          this.nestedValidationErrors[key] = validationResult;
        }
      }
    },

    validateValue(value, validations) {
      if (!validations) return true;

      const {
        required,
        min,
        max,
        pattern,
        custom,
        type,
        enum: enumValues,
      } = validations;

      // Handle undefined/null for required fields
      if (required && (value === undefined || value === null || value === "")) {
        return "This field is required";
      }

      // Skip further validation if value is empty and not required
      if (
        !required &&
        (value === undefined || value === null || value === "")
      ) {
        return true;
      }

      // Validate select fields
      if (this.config?.type === "select" && enumValues) {
        if (!enumValues.includes(value)) {
          return `Please select a valid option`;
        }
      }

      // Validate numbers
      if (this.config?.type === "number") {
        const numValue = Number(value);
        if (isNaN(numValue)) {
          return "Must be a valid number";
        }
        if (min !== undefined && numValue < min) {
          return `Value must be at least ${min}`;
        }
        if (max !== undefined && numValue > max) {
          return `Value must be at most ${max}`;
        }
      }

      // Validate text patterns
      if (pattern && typeof value === "string") {
        try {
          if (!new RegExp(pattern).test(value)) {
            return "Invalid format";
          }
        } catch (e) {
          console.error("Invalid regex pattern:", pattern);
          return "Invalid format";
        }
      }

      // Custom validation
      if (custom && typeof custom === "function") {
        try {
          const customResult = custom(value);
          if (customResult !== true) {
            return customResult || "Invalid value";
          }
        } catch (e) {
          console.error("Custom validation error:", e);
          return "Validation error";
        }
      }

      return true;
    },
  },

  watch: {
    modelValue: {
      immediate: true,
      handler(val) {
        const validationResult = this.validateValue(val);
        this.validationError =
          validationResult === true ? "" : validationResult;
      },
    },
  },
};
</script>
