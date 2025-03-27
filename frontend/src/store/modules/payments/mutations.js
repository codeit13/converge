export default {
  // Plans
  SET_PLANS(state, plans) {
    state.plans = plans;
  },

  // Current order/payment
  SET_CURRENT_ORDER(state, order) {
    state.currentOrder = order;
  },
  SET_ORDER_STATUS(state, status) {
    state.orderStatus = status;
  },

  // Subscription
  SET_SUBSCRIPTION_STATUS(state, status) {
    state.subscriptionStatus = status;
  },

  // Payment history
  SET_PAYMENT_HISTORY(state, history) {
    state.paymentHistory = history;
  },

  // UI states
  SET_ERROR(state, error) {
    state.error = error;
  },
  SET_LOADING(state, isLoading) {
    state.isLoading = isLoading;
  },

  // Reset states
  RESET_PAYMENT_STATE(state) {
    state.currentOrder = null;
    state.orderStatus = null;
    state.error = null;
  },
  RESET_ALL(state) {
    state.plans = [];
    state.currentOrder = null;
    state.orderStatus = null;
    state.subscriptionStatus = null;
    state.paymentHistory = [];
    state.error = null;
    state.isLoading = false;
  },
};
