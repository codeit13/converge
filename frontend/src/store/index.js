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
    TOASTER_DATA: null,
    isSidebarOpen: true,
  },
  actions,
  mutations,
});
