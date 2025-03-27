<template>
  <div class="max-w-2xl mx-auto my-6 space-y-8">
    <!-- Tabs for Global vs Project Settings -->
    <Tabs v-model="activeTab" class="mb-8">
      <TabsList class="w-full">
        <TabsTrigger value="global" class="px-4 py-2 w-full">
          Global Settings
        </TabsTrigger>
        <TabsTrigger value="project" class="px-4 py-2 w-full">
          App Settings
        </TabsTrigger>
      </TabsList>

      <!-- Global Settings Tab -->
      <TabsContent value="global" class="space-y-6">
        <!-- Global Settings (Dynamic Form) -->
        <Card class="mb-6">
          <CardHeader>
            <CardTitle>Global Settings</CardTitle>
            <CardDescription>
              Customize your global account settings.
            </CardDescription>
          </CardHeader>
          <CardContent class="flex flex-col">
            <div class="space-y-4 mb-4">
              <template
                v-for="(config, key) in settingsConfig.global"
                :key="key"
              >
                <DynamicSettingField
                  v-if="config.active !== false"
                  :modelValue="getSettingValue(key, 'global')"
                  @update:modelValue="
                    (val) => setSettingValue(key, 'global', val)
                  "
                  :config="config"
                />
              </template>
            </div>
            <Button
              variant="outline"
              class="ml-auto"
              :loading="$store.state.isLoading"
              @click="saveGlobalSettings"
            >
              Save Global Settings
            </Button>
          </CardContent>
        </Card>

        <!-- Account Security -->
        <Card class="mb-6">
          <CardHeader>
            <CardTitle>Account Security</CardTitle>
            <CardDescription>
              Update your password and security settings.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form
              @submit.prevent="handleAccountSubmit"
              class="space-y-4 flex flex-col"
            >
              <div class="space-y-2">
                <Label for="currentPassword">Current Password</Label>
                <div class="relative">
                  <Input
                    id="currentPassword"
                    :type="passwordVisibility.current ? 'text' : 'password'"
                    v-model="accountData.currentPassword"
                    class="pr-10"
                  />
                  <button
                    type="button"
                    class="absolute inset-y-0 right-0 flex items-center pr-3"
                    @click="togglePasswordVisibility('current')"
                  >
                    <span
                      v-if="passwordVisibility.current"
                      class="text-gray-500 hover:text-gray-700"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path>
                        <path
                          d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"
                        ></path>
                        <path
                          d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"
                        ></path>
                        <line x1="2" x2="22" y1="2" y2="22"></line>
                      </svg>
                    </span>
                    <span v-else class="text-gray-500 hover:text-gray-700">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <path
                          d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"
                        ></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </span>
                  </button>
                </div>
              </div>
              <div class="space-y-2">
                <Label for="newPassword">New Password</Label>
                <div class="relative">
                  <Input
                    id="newPassword"
                    :type="passwordVisibility.new ? 'text' : 'password'"
                    v-model="accountData.newPassword"
                    class="pr-10"
                  />
                  <button
                    type="button"
                    class="absolute inset-y-0 right-0 flex items-center pr-3"
                    @click="togglePasswordVisibility('new')"
                  >
                    <span
                      v-if="passwordVisibility.new"
                      class="text-gray-500 hover:text-gray-700"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path>
                        <path
                          d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"
                        ></path>
                        <path
                          d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"
                        ></path>
                        <line x1="2" x2="22" y1="2" y2="22"></line>
                      </svg>
                    </span>
                    <span v-else class="text-gray-500 hover:text-gray-700">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <path
                          d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"
                        ></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </span>
                  </button>
                </div>
              </div>
              <div class="space-y-2">
                <Label for="confirmPassword">Confirm New Password</Label>
                <div class="relative">
                  <Input
                    id="confirmPassword"
                    :type="passwordVisibility.confirm ? 'text' : 'password'"
                    v-model="accountData.confirmPassword"
                    class="pr-10"
                  />
                  <button
                    type="button"
                    class="absolute inset-y-0 right-0 flex items-center pr-3"
                    @click="togglePasswordVisibility('confirm')"
                  >
                    <span
                      v-if="passwordVisibility.confirm"
                      class="text-gray-500 hover:text-gray-700"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path>
                        <path
                          d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"
                        ></path>
                        <path
                          d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"
                        ></path>
                        <line x1="2" x2="22" y1="2" y2="22"></line>
                      </svg>
                    </span>
                    <span v-else class="text-gray-500 hover:text-gray-700">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <path
                          d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"
                        ></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </span>
                  </button>
                </div>
              </div>
              <Button type="submit" :loading="$store.state.isLoading">
                Update Password
              </Button>
            </form>
          </CardContent>
        </Card>
      </TabsContent>

      <!-- Project Settings Tab -->
      <TabsContent value="project" class="space-y-6">
        <!-- Project Settings (Dynamic Form) -->
        <Card class="mb-6">
          <CardHeader>
            <CardTitle>App Settings</CardTitle>
            <CardDescription
              >Customize the settings specific to this app.</CardDescription
            >
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <template
                v-for="(config, key) in settingsConfig.project"
                :key="key"
              >
                <DynamicSettingField
                  v-if="config.active !== false"
                  :modelValue="getSettingValue(key, 'project')"
                  @update:modelValue="
                    (val) => setSettingValue(key, 'project', val)
                  "
                  :config="config"
                />
              </template>
            </div>
            <Button
              variant="outline"
              :loading="$store.state.isLoading"
              @click="saveProjectSettings"
            >
              Save App Settings
            </Button>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>

    <!-- Danger Zone -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle>Danger Zone</CardTitle>
        <CardDescription>Irreversible and destructive actions.</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-4">
          <p class="text-sm text-muted-foreground">
            Once you delete your account, there is no going back. Please be
            certain.
          </p>
          <Button
            variant="destructive"
            class="bg-red-600 hover:bg-red-700"
            :loading="$store.state.isLoading"
            @click="handleDeleteAccount"
          >
            Delete Account
          </Button>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import DynamicSettingField from "@/components/DynamicSettingField.vue";
</script>

<script>
import { setTheme, getTheme } from "@/utils/theme";
import { PROJECT_ID } from "@/utils/constants";
import { mapState } from "vuex";

export default {
  name: "Settings",
  data() {
    return {
      activeTab: "global",
      settingsConfig: {
        global: {
          theme: {
            type: "select",
            label: "Theme",
            dontSendToApi: true,
            value: getTheme(),
            options: [
              { label: "Light", value: "light" },
              { label: "Dark", value: "dark" },
              { label: "System", value: "system" },
            ],
            description: "Choose your preferred theme",
            active: true,
            validations: {
              required: true,
              type: "string",
              enum: ["light", "dark", "system"],
            },
            placeholder: "Select theme",
          },
          notifications: {
            type: "object",
            label: "Notifications",
            description: "Configure your notification preferences",
            active: true,
            fields: {
              email: {
                type: "boolean",
                label: "Email",
                value: true,
                description: "Receive email notifications",
                validations: { required: true },
                active: true,
              },
              push: {
                type: "boolean",
                label: "Push",
                value: false,
                description: "Receive push notifications",
                validations: { required: true },
                active: true,
              },
              sms: {
                type: "boolean",
                label: "SMS",
                value: false,
                description: "Receive SMS notifications",
                validations: { required: true },
                active: false,
              },
            },
          },
        },
        project: {
          notifications: {
            type: "object",
            label: "Notifications",
            description: "Project-specific notification settings",
            active: true,
            fields: {
              email: {
                type: "boolean",
                label: "Email",
                value: true,
                description: "Project email notifications",
                validations: { required: true },
                active: true,
              },
              push: {
                type: "boolean",
                label: "Push",
                value: false,
                description: "Project push notifications",
                validations: { required: true },
                active: true,
              },
              sms: {
                type: "boolean",
                label: "SMS",
                value: false,
                description: "Project SMS notifications",
                validations: { required: true },
                active: false,
              },
            },
          },
          data: {
            type: "object",
            label: "Additional Data",
            value: {},
            description: "Additional project data",
            active: true,
            fields: {
              name: {
                type: "text",
                label: "Name",
                value: "",
                description: "Enter the name of the project",
                validations: { required: true },
                active: true,
              },
              bio: {
                type: "text",
                label: "Bio",
                value: "",
                description: "Enter a description for the project",
                validations: { required: true },
                active: true,
              },
            },
          },
          // data: {
          //   type: "textarea",
          //   label: "Additional Data",
          //   value: "",
          //   description: "Additional project data",
          //   active: true,
          //   placeholder: "Enter any additional project information",
          //   rows: 4,
          //   validations: {
          //     pattern: "^[a-zA-Z0-9\s\-_]*$",
          //     custom: (value) => {
          //       if (!value) return true; // Allow empty if not required
          //       if (value.length > 500) return "Maximum 500 characters allowed";
          //       if (!/^[a-zA-Z0-9\s\-_]*$/.test(value)) {
          //         return "Only letters, numbers, spaces, hyphens, and underscores allowed";
          //       }
          //       return true;
          //     },
          //   },
        },
      },
      accountData: {
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
      },
      passwordVisibility: {
        current: false,
        new: false,
        confirm: false,
      },
    };
  },
  computed: {
    ...mapState("auth", ["user"]),
  },
  watch: {
    user: {
      handler(newUser) {
        if (newUser) {
          this.loadSettings();
        }
      },
      immediate: true,
    },
    "settingsConfig.global.theme.value"(newTheme) {
      setTheme(newTheme);
    },
  },
  methods: {
    togglePasswordVisibility(field) {
      this.passwordVisibility[field] = !this.passwordVisibility[field];
    },
    // Extract settings values for API calls
    getSettingsValues(section) {
      const values = {};
      Object.entries(this.settingsConfig[section]).forEach(([key, config]) => {
        if (!config.active || config.dontSendToApi) return;

        if (config.type === "object" && config.fields) {
          values[key] = {};
          Object.entries(config.fields).forEach(([fieldKey, fieldConfig]) => {
            if (fieldConfig.active && fieldConfig.value !== undefined) {
              values[key][fieldKey] = fieldConfig.value;
            }
          });
          // Only include non-empty objects
          if (Object.keys(values[key]).length === 0) {
            delete values[key];
          }
        } else if (config.value !== undefined) {
          // Only include defined values
          values[key] = config.value;
        }
      });
      return values;
    },

    loadSettings() {
      const user = this.user;
      if (!user) return;

      // Process each section (global and project)
      Object.keys(this.settingsConfig).forEach((section) => {
        // Get settings source based on section
        const settingsSource =
          section === "global"
            ? user.settings
            : section === "project"
            ? user.projects?.find(
                (p) => p.project?._id?.toString() === PROJECT_ID.toString()
              )?.settings
            : null;

        if (!settingsSource) return;

        // Process each setting in the section
        Object.entries(this.settingsConfig[section]).forEach(
          ([key, config]) => {
            // Special handling for theme (always active)
            if (key === "theme") {
              config.active = true;
              config.value = settingsSource.theme || getTheme();
              return;
            }

            // For other settings, check if they exist in the source
            const settingExists = settingsSource[key] !== undefined;
            config.active = settingExists;

            if (!settingExists) return;

            // Handle object type settings (e.g., notifications)
            if (config.type === "object" && config.fields) {
              Object.entries(config.fields).forEach(
                ([fieldKey, fieldConfig]) => {
                  const fieldExists =
                    settingsSource[key]?.[fieldKey] !== undefined;
                  fieldConfig.active = fieldExists;

                  if (fieldExists) {
                    fieldConfig.value = settingsSource[key][fieldKey];
                  }
                }
              );
            } else {
              // Handle simple settings
              config.value = settingsSource[key];
            }
          }
        );
      });
    },

    getSettingValue(key, section) {
      const setting = this.settingsConfig[section][key];
      if (!setting || !setting.active) {
        return null;
      }

      if (setting.type === "object" && setting.fields) {
        // For object type settings (e.g., notifications)
        const fields = {};
        Object.entries(setting.fields).forEach(([fieldKey, fieldConfig]) => {
          if (fieldConfig.active) {
            fields[fieldKey] = fieldConfig.value;
          }
        });
        return fields;
      }

      // For simple settings (e.g., theme)
      return setting.value;
    },

    setSettingValue(key, section, value) {
      const setting = this.settingsConfig[section][key];
      if (!setting) return;

      setting.active = true;
      if (setting.type === "object" && setting.fields) {
        // For object type settings (e.g., notifications)
        Object.entries(value).forEach(([fieldKey, fieldValue]) => {
          const fieldConfig = setting.fields[fieldKey];
          if (fieldConfig) {
            fieldConfig.active = true;
            fieldConfig.value = fieldValue;
          }
        });
      } else {
        // For simple settings (e.g., theme)
        setting.value = value;
      }

      // Auto-save settings after each change
      if (section === "global") {
        this.saveGlobalSettings();
      } else if (section === "project") {
        this.saveProjectSettings();
      }
    },

    async handleAccountSubmit() {
      try {
        if (!this.accountData.currentPassword) {
          throw new Error("Current password is required");
        }
        if (!this.accountData.newPassword) {
          throw new Error("New password is required");
        }
        if (this.accountData.newPassword.length < 8) {
          throw new Error("Password must be at least 8 characters");
        }
        if (this.accountData.newPassword !== this.accountData.confirmPassword) {
          throw new Error("Passwords do not match");
        }

        const data = await this.$store.dispatch("auth/updatePassword", {
          currentPassword: this.accountData.currentPassword,
          newPassword: this.accountData.newPassword,
          confirmPassword: this.accountData.confirmPassword,
        });

        if (data?.status) {
          // Clear password fields
          this.accountData = {
            currentPassword: "",
            newPassword: "",
            confirmPassword: "",
          };
        }
      } catch (error) {
        this.$store.dispatch("auth/showNotification", {
          type: "error",
          message: error?.response?.data?.message || error.message,
        });
      }
    },

    async saveGlobalSettings() {
      try {
        const settings = this.getSettingsValues("global");
        await this.$store.dispatch("auth/updateGlobalSettings", settings);

        // Update local settings with API response
        if (this.user?.settings) {
          this.loadSettings();
        }
      } catch (error) {
        this.$store.dispatch("auth/showNotification", {
          type: "error",
          message:
            error?.response?.data?.error?.message ||
            "Failed to update global settings",
        });
      }
    },

    async saveProjectSettings() {
      const settings = this.getSettingsValues("project");
      await this.$store.dispatch("auth/updateProjectSettings", settings);

      const projectIndex = this.user?.projects?.findIndex(
        (p) => p.project?._id?.toString() === PROJECT_ID.toString()
      );

      if (projectIndex !== -1) {
        this.user.projects[projectIndex].settings = settings;
      }

      // Update local settings with API response
      if (this.user?.projects?.[projectIndex]?.settings) {
        this.loadSettings();
      }
    },

    async handleDeleteAccount() {
      const confirmed = window.confirm(
        "Are you sure you want to delete your account? This action cannot be undone."
      );
      if (confirmed) {
        try {
          await this.$store.dispatch("auth/deleteAccount");
          this.$store.dispatch("auth/showNotification", {
            type: "success",
            message: "Account deleted successfully",
          });
          this.$router.push("/auth/login");
        } catch (error) {
          this.$store.dispatch("auth/showNotification", {
            type: "error",
            message:
              error?.response?.data?.error?.message ||
              "Failed to delete account",
          });
        }
      }
    },
  },
};
</script>
