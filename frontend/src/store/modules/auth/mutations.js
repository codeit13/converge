import { PROJECT_ID } from "@/utils/constants";

export default {
  SET_USER(state, user) {
    state.user = user;

    if (PROJECT_ID) {
      state.currentProject = user.projects?.find(
        (p) => p?.project?._id?.toString() === PROJECT_ID.toString()
      );
    }
  },
  SET_AUTH_TOKENS(state, payload) {
    state.TOKENS = payload;
  },
};
