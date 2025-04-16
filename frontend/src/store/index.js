import { createStore } from "vuex";
import actions from "./actions";
import mutations from "./mutations";
import auth from "./modules/auth";
import payments from "./modules/payments";

export default createStore({
  modules: {
    auth,
    payments,
  },
  state: {
    isLoading: false,
    documents: [],
    TOASTER_DATA: null,
    isSidebarOpen: true,
    history: null,
    availableTools: null,
    JWT_TOKEN: null,
    toaster: {
      show: false,
      type: "success",
      message: "",
      description: "",
    },
    chatSessions: [],
    currentChatId: null,
    currentChatMessages: [],
    // Analytics-related state
    analyticsSummary: null,
    chatDistribution: null,
  },
  actions,
  mutations,
});
