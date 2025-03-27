<template>
  <header
    class="border-b bg-background dark:bg-dark-600 bg-light-100 dark:bg-glossy-dark dark:backdrop-blur-md bg-glossy-light backdrop-blur-md flex h-16 shrink-0 items-center gap-2 sticky top-0 z-[9999]"
  >
    <div class="container mx-auto flex w-full items-center gap-3 px-4 md:px-6">
      <Button
        variant="ghost"
        size="icon"
        @click="$router.push('/')"
        class="-ml-2"
      >
        <ArrowLeft class="h-4 w-4" />
      </Button>
      <Separator orientation="vertical" class="h-4" />
      <Breadcrumb class="w-full">
        <BreadcrumbList class="flex items-center gap-1">
          <!-- Home link always visible -->
          <BreadcrumbItem class="flex items-center">
            <BreadcrumbLink
              @click="navigateToHome"
              class="group flex items-center gap-1.5 rounded-md px-2 py-1 hover:bg-muted"
            >
              <Home
                class="h-4 w-4 text-muted-foreground transition-colors group-hover:text-primary"
              />
              <span class="text-sm font-medium">Dashboard</span>
            </BreadcrumbLink>
          </BreadcrumbItem>

          <!-- Dynamic breadcrumbs -->
          <template v-for="(crumb, index) in breadcrumbs" :key="crumb.path">
            <template v-if="shouldShowCrumb(index)">
              <!-- Separator with dots for skipped items -->
              <BreadcrumbItem
                v-if="showDots(index)"
                class="hidden md:block px-1"
              >
                <span class="flex items-center gap-0.5">
                  <span
                    class="h-1 w-1 rounded-full bg-muted-foreground/50"
                  ></span>
                  <span
                    class="h-1 w-1 rounded-full bg-muted-foreground/50"
                  ></span>
                  <span
                    class="h-1 w-1 rounded-full bg-muted-foreground/50"
                  ></span>
                </span>
              </BreadcrumbItem>

              <!-- Regular crumb -->
              <BreadcrumbItem class="flex items-center">
                <ChevronRight
                  class="h-4 w-4 text-muted-foreground/50 hidden md:block"
                  :class="{ hidden: index === 0 }"
                />
                <BreadcrumbLink
                  v-if="index < breadcrumbs.length - 1"
                  @click="navigateTo(crumb.path)"
                  class="group hidden md:flex items-center gap-2 rounded-md px-3 py-1.5 hover:bg-muted"
                >
                  <component
                    :is="getRouteIcon(crumb.path)"
                    class="h-4 w-4 text-muted-foreground transition-colors group-hover:text-primary"
                  />
                  <span class="text-sm font-medium">
                    {{ crumb.name || formatRouteName(crumb.path) }}
                  </span>
                </BreadcrumbLink>
                <div
                  v-else
                  class="flex items-center gap-2 rounded-md px-3 py-1.5 text-muted-foreground"
                >
                  <component :is="getRouteIcon(crumb.path)" class="h-4 w-4" />
                  <span class="text-sm font-medium">
                    {{ crumb.name || formatRouteName(crumb.path) }}
                  </span>
                </div>
              </BreadcrumbItem>
            </template>
          </template>
        </BreadcrumbList>
      </Breadcrumb>
    </div>
  </header>
</template>

<script setup>
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
} from "@/components/ui/breadcrumb";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  ArrowLeft,
  BookOpen,
  ChevronRight,
  Home,
  Settings2,
  User,
} from "lucide-vue-next";
</script>

<script>
export default {
  computed: {
    breadcrumbs() {
      return this.$route.matched
        .filter((route) => route.path && route.path !== "/")
        .map((route) => ({
          name: route.name,
          path: route.path,
        }));
    },
  },

  methods: {
    getRouteIcon(path) {
      const routeIcons = {
        "/profile": User,
        "/settings": Settings2,
        default: BookOpen,
      };
      return routeIcons[path] || routeIcons.default;
    },

    shouldShowCrumb(index) {
      if (index === 0 || index === this.breadcrumbs.length - 1) return true;
      if (this.isMobile) return false;
      return true;
    },

    showDots(index) {
      return (
        index === this.breadcrumbs.length - 1 && this.breadcrumbs.length > 2
      );
    },

    formatRouteName(path) {
      return (
        path
          .split("/")
          .filter(Boolean)
          .pop()
          ?.split("-")
          .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
          .join(" ") || "Dashboard"
      );
    },

    navigateToHome() {
      if (this.$route.path !== "/") {
        this.$router.push("/");
      }
    },

    navigateTo(path) {
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    },
  },
};
</script>
