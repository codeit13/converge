export default {
  SET_IS_LOADING(state, payload) {
    state.isLoading = payload;
  },
  SET_TOASTER_DATA(state, payload) {
    state.TOASTER_DATA = payload;
  },
  SET_SIDEBAR_OPEN(state, payload) {
    state.isSidebarOpen = payload;
  },
};
