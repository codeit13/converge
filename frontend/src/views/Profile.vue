<template>
  <Card class="max-w-2xl mx-auto">
    <CardHeader>
      <CardTitle>Profile</CardTitle>
      <CardDescription>Manage your personal information.</CardDescription>
    </CardHeader>
    <CardContent>
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div class="space-y-4">
          <div class="space-y-2">
            <Label>Profile picture</Label>
            <div class="flex items-center gap-4">
              <Avatar class="h-24 w-24">
                <AvatarImage :src="formData.profile.avatar" />
                <AvatarFallback>{{ getInitials }}</AvatarFallback>
              </Avatar>
              <Button variant="outline" @click="handleImageUpload">
                Change picture
              </Button>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="name">Full Name</Label>
              <Input id="name" v-model="formData.name" placeholder="John Doe" />
            </div>

            <div class="space-y-2">
              <Label for="email">Email</Label>
              <Input
                id="email"
                type="email"
                v-model="formData.email"
                placeholder="john@example.com"
                readonly
              />
              <p class="text-sm text-muted-foreground">
                Email cannot be changed
              </p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="phone">Phone</Label>
              <Input
                id="phone"
                type="tel"
                v-model="formData.profile.phone"
                placeholder="+1234567890"
              />
            </div>
            <div class="space-y-2">
              <Label for="language">Language</Label>
              <Select v-model="formData.profile.language">
                <SelectTrigger>
                  <SelectValue placeholder="Select your language" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Languages</SelectLabel>
                    <SelectItem
                      v-for="lang in languages"
                      :key="lang.code"
                      :value="lang.code"
                    >
                      {{ lang.name }}
                    </SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div class="grid grid-cols-1 gap-4">
            <div class="space-y-2">
              <Label for="timezone">Timezone</Label>
              <Select v-model="formData.profile.timezone">
                <SelectTrigger>
                  <SelectValue placeholder="Select your timezone" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Timezones</SelectLabel>
                    <SelectItem v-for="tz in timezones" :key="tz" :value="tz">
                      {{ tz }}
                    </SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div class="space-y-2">
            <Label for="bio">Bio</Label>
            <Textarea
              id="bio"
              v-model="formData.profile.bio"
              placeholder="Tell us about yourself"
              rows="4"
            />
          </div>
        </div>

        <div
          class="flex flex-col-reverse sm:flex-row justify-end gap-3 sm:gap-4"
        >
          <Button
            v-if="hasChanges"
            variant="outline"
            type="button"
            @click="resetForm"
          >
            Reset
          </Button>
          <Button v-if="hasChanges" type="submit"> Save changes </Button>
        </div>
      </form>
    </CardContent>
  </Card>
</template>

<!-- Component imports using script setup -->
<script setup>
import PageWrapper from "@/components/layout/PageWrapper.vue";
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
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { setTheme, getTheme } from "@/utils/theme";
</script>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("auth", ["user"]),
  },

  watch: {
    user: {
      immediate: true,
      handler(val) {
        if (!val) {
          this.$router.push("/auth/login");
        } else {
          this.loadUserProfile();
        }
      },
    },
  },

  data() {
    return {
      // Language options
      languages: [
        { code: "en", name: "English" },
        { code: "es", name: "Spanish" },
        { code: "fr", name: "French" },
        { code: "de", name: "German" },
        { code: "it", name: "Italian" },
        { code: "pt", name: "Portuguese" },
        { code: "ru", name: "Russian" },
        { code: "ja", name: "Japanese" },
        { code: "ko", name: "Korean" },
        { code: "zh", name: "Chinese" },
      ],
      // Timezone options
      timezones: [
        "UTC",
        "UTC+1",
        "UTC+2",
        "UTC+3",
        "UTC+4",
        "UTC+5",
        "UTC+5:30",
        "UTC+6",
        "UTC+7",
        "UTC+8",
        "UTC+9",
        "UTC+10",
        "UTC+11",
        "UTC+12",
        "UTC-1",
        "UTC-2",
        "UTC-3",
        "UTC-4",
        "UTC-5",
        "UTC-6",
        "UTC-7",
        "UTC-8",
        "UTC-9",
        "UTC-10",
        "UTC-11",
        "UTC-12",
      ],
      formData: {
        name: "",
        email: "",
        profile: {
          avatar: "",
          phone: "",
          bio: "",
          language: "en",
          timezone: "UTC",
        },
      },
      originalData: null,
    };
  },

  computed: {
    ...mapState("auth", ["user"]),

    getInitials() {
      return (
        this.formData.name
          ?.split(" ")
          .map((n) => n[0])
          .join("")
          .toUpperCase() || "U"
      );
    },

    hasChanges() {
      if (!this.originalData) return false;

      // Compare name and email
      if (this.formData.name !== this.originalData.name) return true;
      if (this.formData.email !== this.originalData.email) return true;

      // Compare profile fields
      const profileFields = ["avatar", "phone", "bio", "language", "timezone"];
      return profileFields.some(
        (field) =>
          this.formData.profile[field] !== this.originalData.profile[field]
      );
    },
  },

  watch: {
    user: {
      immediate: true,
      handler(val) {
        if (!val) {
          this.$router.push("/auth/login");
        } else if (val) {
          this.loadUserProfile();
        }
      },
    },
  },

  methods: {
    loadUserProfile() {
      if (this.user) {
        const userData = {
          name: this.user.name || "",
          email: this.user.email || "",
          profile: {
            avatar: this.user.profile?.avatar || "",
            phone: this.user.profile?.phone || "",
            bio: this.user.profile?.bio || "",
            language: this.user.profile?.language || "en",
            timezone: this.user.profile?.timezone || "UTC",
          },
        };
        this.formData = JSON.parse(JSON.stringify(userData));
        this.originalData = JSON.parse(JSON.stringify(userData));
      }
    },

    async handleSubmit() {
      try {
        // Only send changed fields
        const changedFields = {};

        Object.keys(this.formData).forEach((key) => {
          if (key === "profile") {
            Object.keys(this.formData.profile).forEach((profileKey) => {
              if (
                JSON.stringify(this.formData.profile[profileKey]) !==
                JSON.stringify(this.originalData.profile[profileKey])
              ) {
                changedFields[profileKey] = this.formData.profile[profileKey];
              }
            });
          } else if (
            JSON.stringify(this.formData[key]) !==
            JSON.stringify(this.originalData[key])
          ) {
            changedFields[key] = this.formData[key];
          }
        });

        if (Object.keys(changedFields).length > 0) {
          const response = await this.$store.dispatch(
            "auth/updateProfile",
            changedFields
          );
          if (response?.status) {
            this.originalData = { ...this.formData };
          }
        }
      } catch (error) {
        this.$store.commit(
          "SET_TOASTER_DATA",
          {
            type: "error",
            message: "Error",
            description:
              error?.response?.data?.message || "Failed to update profile",
          },
          { root: true }
        );
      }
    },

    async handleImageUpload() {
      try {
        const input = document.createElement("input");
        input.type = "file";
        input.accept = "image/*";

        input.onchange = async (e) => {
          const file = e.target.files[0];
          if (!file) return;

          // Check file size (5MB limit)
          if (file.size > 5 * 1024 * 1024) {
            this.$store.commit(
              "SET_TOASTER_DATA",
              {
                type: "error",
                message: "Image size should not exceed 5MB",
              },
              { root: true }
            );
            return;
          }

          // Convert to base64
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = async () => {
            try {
              const base64Image = reader.result;
              await this.$store.dispatch("auth/updateProfile", {
                avatar: base64Image,
              });
              this.formData.profile.avatar = base64Image;
              this.originalData.profile.avatar = base64Image;

              this.$store.commit(
                "SET_TOASTER_DATA",
                {
                  type: "success",
                  message: "Profile picture updated successfully",
                },
                { root: true }
              );
            } catch (error) {
              this.$store.commit(
                "SET_TOASTER_DATA",
                {
                  type: "error",
                  message:
                    error?.response?.data?.message || "Failed to upload image",
                },
                { root: true }
              );
            }
          };
        };

        input.click();
      } catch (error) {
        this.$store.commit(
          "SET_TOASTER_DATA",
          {
            type: "error",
            message: "Failed to handle image upload",
          },
          { root: true }
        );
      }
    },

    resetForm() {
      this.formData = { ...this.originalData };
      this.$store.commit(
        "SET_TOASTER_DATA",
        {
          type: "info",
          message: "Form reset to original values",
        },
        { root: true }
      );
    },
  },
};
</script>
