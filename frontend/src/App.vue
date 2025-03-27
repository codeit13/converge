<template>
  <!-- Layout with sidebar (default) -->
  <Sidebar v-if="shouldShowSidebar">
    <PageWrapper>
      <router-view v-slot="{ Component }">
        <transition
          :name="transitionName"
          mode="out-in"
          @before-leave="beforeLeave"
          @enter="enter"
          @after-enter="afterEnter"
        >
          <component :is="Component" />
        </transition>
      </router-view>
    </PageWrapper>
  </Sidebar>

  <!-- Layout without sidebar and top header -->
  <template v-else-if="hideTopHeader">
    <PageWrapper>
      <router-view v-slot="{ Component }">
        <transition
          :name="transitionName"
          mode="out-in"
          @before-leave="beforeLeave"
          @enter="enter"
          @after-enter="afterEnter"
        >
          <component :is="Component" />
        </transition>
      </router-view>
    </PageWrapper>
  </template>

  <!-- Layout without sidebar -->
  <template v-else>
    <StandaloneBreadcrumb />
    <PageWrapper>
      <router-view v-slot="{ Component }">
        <transition
          :name="transitionName"
          mode="out-in"
          @before-leave="beforeLeave"
          @enter="enter"
          @after-enter="afterEnter"
        >
          <component :is="Component" />
        </transition>
      </router-view>
    </PageWrapper>
  </template>

  <Toaster
    class="pointer-events-auto"
    theme="dark"
    position="top-right"
    richColors
    :duration="6000"
    :expand="true"
  />
  <Loader />
</template>

<script setup>
import Sidebar from "@/components/Sidebar.vue";
import StandaloneBreadcrumb from "@/components/StandaloneBreadcrumb.vue";
import PageWrapper from "@/components/layout/PageWrapper.vue";
import { Toaster } from "@/components/ui/sonner";
</script>

<script>
import { mapState } from "vuex";
import { toast } from "vue-sonner";
import Loader from "./components/Loader.vue";
import { initTheme } from "@/utils/theme";

export default {
  data() {
    return {
      tokenCheckInterval: null,
      transitionName: "slide-right",
      // Routes that should NOT show the sidebar
      // All other routes will show the sidebar by default
      noSidebarRoutes: [
        "/auth",
        "/auth/login",
        "/auth/register",
        "/profile",
        "/settings",
        "/pricing",
      ],
      noTopHeaderRoutes: ["/auth", "/auth/login", "/auth/register"],
    };
  },
  computed: {
    ...mapState(["TOASTER_DATA"]),
    ...mapState("auth", ["TOKENS"]),

    // Determine if sidebar should be shown based on current route
    // By default, show sidebar for all routes except those in noSidebarRoutes
    shouldShowSidebar() {
      const currentPath = this.$route.path;
      return !this.noSidebarRoutes.some((path) => currentPath.startsWith(path));
    },
    hideTopHeader() {
      const currentPath = this.$route.path;
      return this.noTopHeaderRoutes.some((path) =>
        currentPath.startsWith(path)
      );
    },
  },
  watch: {
    $route(to, from) {
      const toDepth = to.path.split("/").length;
      const fromDepth = from.path.split("/").length;
      this.transitionName = toDepth < fromDepth ? "slide-right" : "slide-left";
    },
    TOASTER_DATA() {
      if (this.TOASTER_DATA) {
        const { type, message, ...options } = this.TOASTER_DATA;

        if (!options?.duration) options.duration = 6000;

        switch (type) {
          case "success":
            toast.success(message, options);
            break;
          case "error":
            toast.error(message, options);
            break;
          case "warning":
            toast.warning(message, options);
            break;
          case "info":
            toast.info(message, options);
            break;
          default:
            toast(message, options);
        }

        // Reset toast data
        setTimeout(() => {
          this.$store.commit("SET_TOASTER_DATA", null, { root: true });
        }, 100);
      }
    },
  },
  methods: {
    beforeLeave(el) {
      el.style.position = "absolute";
      el.style.width = "100%";
    },
    enter(el) {
      el.style.position = "absolute";
      el.style.width = "100%";
    },
    afterEnter(el) {
      el.style.position = "";
      el.style.width = "";
    },
  },

  mounted() {
    // Initialize theme
    initTheme();

    // Set up periodic token refresh check
    this.tokenCheckInterval = setInterval(() => {
      const tokens = JSON.parse(localStorage.getItem("tokens"));
      if (tokens?.access?.token) {
        const tokenExpiry = new Date(tokens.access.expires).getTime();
        const now = new Date().getTime();
        const timeToExpiry = tokenExpiry - now;

        // If token expires in less than 5 minutes, refresh it
        if (timeToExpiry < 300000 && timeToExpiry > 0) {
          this.$store.dispatch("auth/refreshTokens");
        }
      }
    }, 60000); // Check every minute
  },
  unmounted() {
    if (this.tokenCheckInterval) {
      clearInterval(this.tokenCheckInterval);
    }
  },
};
</script>

<style>
/* Route transition effects */
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(60px);
}

.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-60px);
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-60px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(60px);
}
</style>
