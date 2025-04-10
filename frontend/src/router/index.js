import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";

const routes = [
  {
    path: "/",
    name: "Dashboard",
    component: () => import("@/views/Chat.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/analytics",
    name: "Analytics",
    component: () => import("@/views/Analytics.vue"),
    meta: { requiresAuth: false },
  },

  // User Auth & Payment Routes begin here
  {
    path: "/auth/:type?",
    name: "Auth",
    component: () => import("@/views/Auth.vue"),
    meta: { requiresAuth: false, isAuthRoute: true },
  },
  {
    path: "/profile",
    name: "Profile",
    component: () => import("@/views/Profile.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/settings",
    name: "Settings",
    component: () => import("@/views/Settings.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/pricing",
    name: "Pricing",
    component: () => import("@/views/Pricing.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/payment-history",
    name: "PaymentHistory",
    component: () => import("@/views/PaymentHistory.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  // Initialize auth state if not already done
  if (!store.state.auth.user) {
    await store.dispatch("auth/getUserProfile");
  }

  const isAuthenticated = !!store.state.auth.TOKENS?.access?.token;
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const isAuthRoute = to.matched.some((record) => record.meta.isAuthRoute);

  if (requiresAuth && !isAuthenticated) {
    // Redirect to login if auth is required but user is not authenticated
    next({ path: "/auth/login", query: { redirect: to.fullPath } });
  } else if (isAuthRoute && isAuthenticated) {
    // Redirect to home if user is already authenticated and tries to access auth routes
    const redirectPath = store.state.auth.user?.redirectPath;
    if (redirectPath) {
      next({ path: redirectPath });
    } else {
      next({ path: "/" });
    }
  } else {
    next();
  }
});

export default router;
