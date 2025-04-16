export default {
  SET_RAG_DOCUMENTS(state, docs) {
    state.documents = docs;
  },
  SET_IS_LOADING(state, payload) {
    state.isLoading = payload;
  },
  SET_TOASTER_DATA(state, payload) {
    state.TOASTER_DATA = payload;
  },
  SET_SIDEBAR_OPEN(state, payload) {
    state.isSidebarOpen = payload;
  },
  SET_AVAILABLE_TOOLS(state, payload) {
    state.availableTools = payload;
  },
  SET_HISTORY(state, payload) {
    state.history = payload;
  },
  // Chat-related mutations
  SET_CHAT_SESSIONS(state, payload) {
    state.chatSessions = payload;
  },
  SET_CURRENT_CHAT_MESSAGES(state, payload) {
    state.currentChatMessages = payload;
  },
  REMOVE_CHAT_SESSION(state, chatId) {
    state.chatSessions = state.chatSessions.filter(session => session.chat_id !== chatId);
  },
  ADD_MESSAGE_TO_CURRENT_CHAT(state, message) {
    if (!state.currentChatMessages) {
      state.currentChatMessages = [];
    }
    state.currentChatMessages.push(message);
  },
  CLEAR_CURRENT_CHAT_MESSAGES(state) {
    state.currentChatMessages = [];
  },
  // Analytics mutations
  SET_ANALYTICS_SUMMARY(state, payload) {
    state.analyticsSummary = payload;
  },
  SET_CHAT_DISTRIBUTION(state, payload) {
    state.chatDistribution = payload;
  },
};
