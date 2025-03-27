import axios from "axios";
import { PAYMENTS_AUTH_URL, PROJECT_ID } from "@/utils/constants";
import store from "@/store";

// Create axios instance with interceptors
const authAxios = axios.create();

// Add request interceptor
authAxios.interceptors.request.use(
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

// Add response interceptor
authAxios.interceptors.response.use(
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
        return authAxios(originalRequest);
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
  async getUserProfile({ commit }) {
    try {
      commit("SET_IS_LOADING", true, { root: true });
      const tokens = JSON.parse(localStorage.getItem("tokens"));
      if (tokens?.access?.token) {
        commit("SET_AUTH_TOKENS", tokens);
        const { data } = await authAxios.get(
          `${PAYMENTS_AUTH_URL}/users/profile`
        );
        if (data?.status) {
          commit("SET_USER", data?.data || null);
        } else {
          commit(
            "SET_TOASTER_DATA",
            {
              type: "error",
              message: "Error",
              description: data?.message || "Failed to get user profile",
            },
            { root: true }
          );
        }
      }
    } catch (e) {
      localStorage.removeItem("tokens");
      commit("SET_AUTH_TOKENS", null);
      commit("SET_USER", null);
    } finally {
      commit("SET_IS_LOADING", false, { root: true });
    }
  },

  async refreshTokens({ commit }) {
    try {
      const tokens = JSON.parse(localStorage.getItem("tokens"));
      const { data } = await axios.post(
        `${PAYMENTS_AUTH_URL}/auth/refresh-tokens`,
        {
          refreshToken: tokens?.refresh?.token,
        }
      );
      localStorage.setItem("tokens", JSON.stringify(data.tokens));
      commit("SET_AUTH_TOKENS", data.tokens);
      return data.tokens;
    } catch (e) {
      localStorage.removeItem("tokens");
      commit("SET_AUTH_TOKENS", null);
      commit("SET_USER", null);
      throw e;
    }
  },

  async register({ commit }, { name, email, password }) {
    try {
      commit("SET_IS_LOADING", true, { root: true });
      const { data } = await authAxios.post(
        `${PAYMENTS_AUTH_URL}/auth/register`,
        { name, email, password }
      );

      if (data?.status) {
        localStorage.setItem("tokens", JSON.stringify(data?.data?.tokens));
        commit("SET_AUTH_TOKENS", data?.data?.tokens);
        commit(
          "SET_TOASTER_DATA",
          {
            type: "success",
            message: "Success",
            description: "Registration successful",
          },
          { root: true }
        );
      }
      return data;
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description: e?.response?.data?.message || e.message,
        },
        { root: true }
      );
      throw e;
    } finally {
      commit("SET_IS_LOADING", false, { root: true });
    }
  },

  async login({ commit }, { email, password }) {
    try {
      commit("SET_IS_LOADING", true, { root: true });
      const { data } = await authAxios.post(`${PAYMENTS_AUTH_URL}/auth/login`, {
        email,
        password,
      });

      if (data?.status) {
        localStorage.setItem("tokens", JSON.stringify(data?.data?.tokens));
        commit("SET_AUTH_TOKENS", data?.data?.tokens);
        commit(
          "SET_TOASTER_DATA",
          {
            type: "success",
            message: "Success",
            description: "Login successful",
          },
          { root: true }
        );
      }
      return data;
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description: e?.response?.data?.message || e.message,
        },
        { root: true }
      );
      throw e;
    } finally {
      commit("SET_IS_LOADING", false, { root: true });
    }
  },

  async loginViaGoogle({ commit }, payload) {
    try {
      commit("SET_IS_LOADING", true, { root: true });
      const { data } = await axios.post(
        `${PAYMENTS_AUTH_URL}/auth/login-via-google`,
        payload,
        {
          headers: {
            "x-project-id": PROJECT_ID,
          },
        }
      );

      localStorage.setItem("tokens", JSON.stringify(data.tokens));
      commit("SET_AUTH_TOKENS", data.tokens);
      commit(
        "SET_TOASTER_DATA",
        {
          type: "success",
          message: "Success",
          description: "Login successful",
        },
        { root: true }
      );
    } catch (e) {
      console.error(e);
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description: e?.response?.data?.message || e.message,
        },
        { root: true }
      );
    } finally {
      commit("SET_IS_LOADING", false, { root: true });
    }
  },

  async logout({ commit }, payload) {
    try {
      commit("SET_IS_LOADING", true, { root: true });
      const tokens = JSON.parse(localStorage.getItem("tokens"));
      if (tokens?.refresh?.token) {
        await authAxios.post(`${PAYMENTS_AUTH_URL}/auth/logout`, {
          refreshToken: tokens.refresh.token,
        });
      }
    } catch (e) {
      console.error(e);
    } finally {
      localStorage.removeItem("tokens");
      commit("SET_IS_LOADING", false, { root: true });
      commit("SET_AUTH_TOKENS", null);
      commit("SET_USER", null);
    }
  },

  showNotification({ commit }, payload) {
    commit("SET_TOASTER_DATA", payload, { root: true });
  },

  async updateProfile({ commit }, payload) {
    try {
      commit("SET_IS_LOADING", true, { root: true });

      const { data } = await authAxios.patch(
        `${PAYMENTS_AUTH_URL}/users/profile`,
        payload
      );

      if (data.status) {
        commit("SET_USER", data.data);
      }

      commit(
        "SET_TOASTER_DATA",
        {
          type: data?.status ? "success" : "error",
          message: data?.status ? "Success" : "Error",
          description: data?.message || "Profile updated successfully",
        },
        { root: true }
      );
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description: e?.response?.data?.message || e.message,
        },
        { root: true }
      );
    } finally {
      commit("SET_IS_LOADING", false, { root: true });
    }
  },

  async updateGlobalSettings({ state, commit }, payload) {
    try {
      commit("SET_IS_LOADING", true, { root: true });
      const { data } = await axios.patch(
        `${PAYMENTS_AUTH_URL}/users/settings`,
        { settings: payload },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${state.TOKENS?.access?.token}`,
          },
        }
      );
      if (data?.status) {
        commit("SET_USER", data?.user);
        commit(
          "SET_TOASTER_DATA",
          {
            type: "success",
            message: "Success",
            description: "Settings updated successfully",
          },
          { root: true }
        );
      }
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description: e?.response?.data?.message || e.message,
        },
        { root: true }
      );
    } finally {
      commit("SET_IS_LOADING", false, { root: true });
    }
  },

  async updateProjectSettings({ commit }, payload) {
    try {
      commit("SET_IS_LOADING", true, { root: true });
      const { data } = await authAxios.patch(
        `${PAYMENTS_AUTH_URL}/users/settings`,
        { settings: payload }
      );

      if (data?.status) {
        commit("SET_USER", data?.data);
        commit(
          "SET_TOASTER_DATA",
          {
            type: "success",
            message: "Success",
            description: "Settings updated successfully",
          },
          { root: true }
        );
      }
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description: e?.response?.data?.message || e.message,
        },
        { root: true }
      );
    } finally {
      commit("SET_IS_LOADING", false, { root: true });
    }
  },

  async updatePassword({ commit }, payload) {
    try {
      commit("SET_IS_LOADING", true, { root: true });
      const { data } = await authAxios.patch(
        `${PAYMENTS_AUTH_URL}/users/change-password`,
        payload
      );

      if (data?.status) {
        commit(
          "SET_TOASTER_DATA",
          {
            type: "success",
            message: "Success",
            description: "Password updated successfully",
          },
          { root: true }
        );
      }
      return data;
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description: e?.response?.data?.message || e.message,
        },
        { root: true }
      );
    } finally {
      commit("SET_IS_LOADING", false, { root: true });
    }
  },

  async deleteAccount({ commit }) {
    try {
      commit("SET_IS_LOADING", true, { root: true });
      await authAxios.delete(`${PAYMENTS_AUTH_URL}/users/account`);

      // Clear local storage and state
      localStorage.removeItem("tokens");
      commit("SET_AUTH_TOKENS", null);
      commit("SET_USER", null);

      commit(
        "SET_TOASTER_DATA",
        {
          type: "success",
          message: "Success",
          description: "Account deleted successfully",
        },
        { root: true }
      );
    } catch (e) {
      commit(
        "SET_TOASTER_DATA",
        {
          type: "error",
          message: "Error",
          description: e?.response?.data?.message || e.message,
        },
        { root: true }
      );
    } finally {
      commit("SET_IS_LOADING", false, { root: true });
    }
  },
};
