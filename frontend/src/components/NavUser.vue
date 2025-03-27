<template>
  <SidebarMenu>
    <SidebarMenuItem>
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <SidebarMenuButton
            size="lg"
            class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
          >
            <Avatar class="h-8 w-8 rounded-lg">
              <AvatarImage
                v-if="user?.image"
                :src="user.image"
                :alt="displayName"
              />
              <AvatarFallback
                class="rounded-lg font-bold bg-secondary text-secondary-foreground"
              >
                {{ userInitials }}
              </AvatarFallback>
            </Avatar>
            <div class="grid flex-1 text-left text-sm leading-tight">
              <span class="truncate font-semibold">
                {{ user?.name || user?.email || "Guest" }}
              </span>
              <span class="truncate text-xs">{{ displayEmail }}</span>
            </div>
            <ChevronsUpDown class="ml-auto size-4" />
          </SidebarMenuButton>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          class="w-[--reka-dropdown-menu-trigger-width] min-w-56 rounded-lg"
          :side="isMobile ? 'bottom' : 'right'"
          align="end"
          :side-offset="4"
        >
          <DropdownMenuLabel class="p-0 font-normal">
            <div class="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
              <Avatar class="h-8 w-8 rounded-lg">
                <AvatarImage
                  v-if="user?.image"
                  :src="user.image"
                  :alt="displayName"
                />
                <AvatarFallback
                  class="rounded-lg font-bold bg-secondary text-secondary-foreground"
                >
                  {{ userInitials }}
                </AvatarFallback>
              </Avatar>
              <div class="grid flex-1 text-left text-sm leading-tight">
                <span class="truncate font-semibold">{{ displayName }}</span>
                <span class="truncate text-xs">{{ displayEmail }}</span>
              </div>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />

          <template v-if="user">
            <DropdownMenuGroup>
              <DropdownMenuItem @click="handleUpgrade">
                <Sparkles class="mr-2 h-4 w-4" />
                <span>Upgrade to Pro</span>
              </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuItem @click="handleProfile">
                <User class="mr-2 h-4 w-4" />
                <span>Profile</span>
              </DropdownMenuItem>
              <DropdownMenuItem @click="handleSettings">
                <Bell class="mr-2 h-4 w-4" />
                <span>Settings</span>
              </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="handleLogout">
              <LogOut class="mr-2 h-4 w-4" />
              <span>Log out</span>
            </DropdownMenuItem>
          </template>

          <template v-else>
            <DropdownMenuItem @click="handleLogin">
              <LogIn class="mr-2 h-4 w-4" />
              <span>Log in</span>
            </DropdownMenuItem>
          </template>
        </DropdownMenuContent>
      </DropdownMenu>
    </SidebarMenuItem>
  </SidebarMenu>
</template>

<script setup>
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";
import {
  Bell,
  ChevronsUpDown,
  LogOut,
  Sparkles,
  LogIn,
  User,
} from "lucide-vue-next";

const { isMobile } = useSidebar();
</script>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("auth", ["user", "currentProject"]),
    userInitials() {
      if (!this.user?.email) return "SA";
      return this.user.name
        ? this.user.name
            .split(" ")
            .map((n) => n[0])
            .join("")
            .toUpperCase()
        : this.user.email.substring(0, 2).toUpperCase();
    },
    displayName() {
      return this.user?.name || this.user?.email || "Guest";
    },
    displayEmail() {
      return this.user?.email || "Not logged in";
    },
  },
  methods: {
    async handleLogout() {
      try {
        await this.$store.dispatch("auth/logout");
        this.$router.push("/auth/login");
      } catch (e) {
        console.error("Logout failed:", e);
      }
    },
    handleLogin() {
      this.$router.push("/auth/login");
    },
    handleUpgrade() {
      this.$router.push("/pricing");
    },
    handleProfile() {
      this.$router.push("/profile");
    },
    handleSettings() {
      this.$router.push("/settings");
    },
  },
};
</script>
