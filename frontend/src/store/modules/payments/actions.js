import axios from "axios";
import { PAYMENTS_AUTH_URL, PROJECT_ID } from "@/utils/constants";
import store from "@/store";

// Create an axios instance with auth interceptor
const paymentAxios = axios.create();

// Add request interceptor for authentication
paymentAxios.interceptors.request.use(
  async (config) => {
    config.headers["Content-Type"] = "application/json";
    config.headers["x-project-id"] = PROJECT_ID;
    const tokens = JSON.parse(localStorage.getItem("tokens"));
    if (tokens?.access?.token) {
      config.headers.Authorization = `Bearer ${tokens.access.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for token expiry
paymentAxios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const tokens = JSON.parse(localStorage.getItem("tokens"));
        if (tokens?.refresh?.token) {
          const { data } = await axios.post(
            `${PAYMENTS_AUTH_URL}/auth/refresh-tokens`,
            {
              refreshToken: tokens?.refresh?.token,
            }
          );

          if (data.tokens) {
            localStorage.setItem("tokens", JSON.stringify(data.tokens));
            store.commit("auth/SET_AUTH_TOKENS", data.tokens);
            originalRequest.headers.Authorization = `Bearer ${data.tokens.access.token}`;
          }
        }
        return paymentAxios(originalRequest);
      } catch (err) {
        localStorage.removeItem("tokens");
        store.commit("auth/SET_AUTH_TOKENS", null);
        store.commit("auth/SET_USER", null);
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

export default {
  async fetchPlans({ commit }) {
    try {
      commit("SET_LOADING", true);

      const { data } = await paymentAxios.get(
        `${PAYMENTS_AUTH_URL}/projects/${PROJECT_ID}`
      );
      commit("SET_PLANS", data.plans);
    } catch (error) {
      const errorMsg =
        error?.response?.data?.message ||
        "Failed to load payment plans. Please try again later.";
      commit("SET_ERROR", errorMsg);
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description: errorMsg,
        },
        { root: true }
      );
      throw error;
    } finally {
      commit("SET_LOADING", false);
    }
  },
  async createPayment({ commit }, { planId, gateway }) {
    try {
      commit("SET_LOADING", true);
      const { data } = await paymentAxios.post(
        `${PAYMENTS_AUTH_URL}/payments/create`,
        { planId, gateway }
      );
      commit("SET_CURRENT_ORDER", data);
      return data;
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description:
            e?.response?.data?.message ||
            "Failed to create payment. Please try again.",
        },
        { root: true }
      );
    } finally {
      commit("SET_LOADING", false);
    }
  },

  async verifyPayment({ commit }, payload) {
    try {
      commit("SET_LOADING", true);
      const { data } = await paymentAxios.post(
        `${PAYMENTS_AUTH_URL}/payments/verify`,
        payload
      );
      commit("SET_ORDER_STATUS", "success");
      commit(
        "SET_TOASTER_DATA",
        {
          type: "success",
          message: "Success",
          description: "Payment verified successfully!",
        },
        { root: true }
      );
      return data;
    } catch (e) {
      commit("SET_ORDER_STATUS", "failed");
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description:
            e?.response?.data?.message ||
            "Payment verification failed. Please contact support.",
        },
        { root: true }
      );
    } finally {
      commit("SET_LOADING", false);
    }
  },

  async getSubscriptionStatus({ commit }) {
    try {
      commit("SET_LOADING", true);
      const response = await paymentAxios.get(
        `${PAYMENTS_AUTH_URL}/payments/subscription/status`
      );

      if (response.data.status) {
        const subscriptionData = {
          status: response.data.data.status,
          currentPlan: response.data.data.currentPlan,
          paymentMethod: response.data.data.paymentMethod,
          usage: response.data.data.usage,
          metrics: response.data.data.metrics,
          recommendations: response.data.data.recommendations,
          securityContext: response.data.data.securityContext,
        };
        commit("SET_SUBSCRIPTION_STATUS", subscriptionData);
        return subscriptionData;
      } else {
        throw new Error(
          response.data.message || "Failed to fetch subscription status"
        );
      }
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description:
            e?.response?.data?.message ||
            e.message ||
            "Failed to fetch subscription status.",
        },
        { root: true }
      );
    } finally {
      commit("SET_LOADING", false);
    }
  },

  async getPaymentHistory({ commit }, queryParams) {
    try {
      commit("SET_LOADING", true);
      const queryString = new URLSearchParams(queryParams).toString();
      const { data } = await paymentAxios.get(
        `${PAYMENTS_AUTH_URL}/payments/history?${queryString}`
      );
      commit("SET_PAYMENT_HISTORY", data);
      return data;
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description:
            e?.response?.data?.message || "Failed to fetch payment history.",
        },
        { root: true }
      );
    } finally {
      commit("SET_LOADING", false);
    }
  },

  async initiateRefund({ commit }, { paymentId, reason }) {
    try {
      commit("SET_LOADING", true);
      const { data } = await paymentAxios.post(
        `${PAYMENTS_AUTH_URL}/payments/refund`,
        { paymentId, reason }
      );
      commit(
        "SET_TOASTER_DATA",
        {
          type: "success",
          message: "Success",
          description: "Refund initiated successfully!",
        },
        { root: true }
      );
      return data;
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description:
            e?.response?.data?.message || "Failed to initiate refund.",
        },
        { root: true }
      );
    } finally {
      commit("SET_LOADING", false);
    }
  },
};
