import actions from "./actions.js";
import mutations from "./mutations.js";

export default {
  namespaced: true,
  state: {
    plans: [],
    currentOrder: null,
    orderStatus: null,
    subscriptionStatus: null,
    paymentHistory: [],
    error: null,
  },
  actions,
  mutations,
};
