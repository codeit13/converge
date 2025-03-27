import actions from "./actions.js";
import mutations from "./mutations.js";

export default {
  namespaced: true,
  state: {
    user: null,
    currentProject: null,
    TOKENS:
      localStorage.getItem("tokens") === null
        ? null
        : JSON.parse(localStorage.getItem("tokens")),
  },
  actions,
  mutations,
};
