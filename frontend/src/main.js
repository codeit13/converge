import { createApp } from "vue";

import { MotionPlugin } from "@vueuse/motion";
import vue3GoogleLogin from "vue3-google-login";

import "./assets/index.css";
import router from "./router/index.js";
import store from "./store/index.js";
import externalLinks from "./directives/external-links.js";

import App from "./App.vue";

const app = createApp(App);

app.directive("external-links", externalLinks);

app.use(vue3GoogleLogin, {
  clientId:
    "648188226834-no9eddcthqh34420hvo3hc09vakt67au.apps.googleusercontent.com",
});

app.use(store).use(router).use(MotionPlugin);

app.mount("#app");
