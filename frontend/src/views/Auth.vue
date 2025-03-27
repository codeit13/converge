<template>
  <div class="flex flex-col gap-6 h-screen">
    <div class="relative w-[85%] md:w-[50%] m-auto">
      <transition
        enter-active-class="transition-all duration-200 cubic-bezier(0.4, 0, 0.2, 1)"
        leave-active-class="transition-all duration-200 cubic-bezier(0.4, 0, 0.2, 1)"
        mode="out-in"
      >
        <div :key="authType">
          <Card
            class="overflow-hidden w-full"
            v-motion
            :initial="{
              opacity: 0,
              y: authType === 'LOGIN' ? -40 : 40,
              scale: 0.1,
              rotateX: authType === 'LOGIN' ? '15deg' : '-15deg',
            }"
            :enter="{
              opacity: 1,
              y: 0,
              scale: 1,
              rotateX: '0deg',
              transition: {
                duration: 600,
                ease: [0.4, 0, 0.2, 1],
              },
            }"
            :leave="{
              opacity: 0,
              y: authType === 'LOGIN' ? 40 : -40,
              scale: 0.1,
              rotateX: authType === 'LOGIN' ? '-10deg' : '10deg',
              transition: {
                duration: 600,
                ease: [0.4, 0, 0.2, 1],
              },
            }"
            v-show="authType == 'REGISTER'"
          >
            <CardContent class="grid p-0 md:grid-cols-2">
              <form @submit.prevent="register" class="p-6 md:p-8">
                <div class="flex flex-col gap-6">
                  <div class="flex flex-col items-center text-center">
                    <h1 class="text-2xl font-bold">Create an account</h1>
                    <p class="text-balance text-muted-foreground">
                      Sign up to get started
                    </p>
                  </div>
                  <div class="grid gap-2">
                    <Label for="name">Name</Label>
                    <Input
                      id="register-name"
                      type="text"
                      v-model="registerName"
                      placeholder="john.agent"
                      required
                    />
                    <Label for="email">Email</Label>
                    <Input
                      id="register-email"
                      type="email"
                      v-model="registerEmail"
                      placeholder="agent@ai.com"
                      required
                    />
                  </div>
                  <div class="grid gap-2">
                    <div class="flex items-center">
                      <Label for="password">Password</Label>
                    </div>
                    <div class="relative">
                      <Input
                        id="register-password"
                        v-model="registerPassword"
                        :type="passwordVisibility.register ? 'text' : 'password'"
                        placeholder="*************"
                        class="pr-10"
                        required
                      />
                      <button 
                        type="button" 
                        class="absolute inset-y-0 right-0 flex items-center pr-3"
                        @click="togglePasswordVisibility('register')"
                      >
                        <span v-if="passwordVisibility.register" class="text-gray-500 hover:text-gray-700">
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"></path><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"></path><line x1="2" x2="22" y1="2" y2="22"></line></svg>
                        </span>
                        <span v-else class="text-gray-500 hover:text-gray-700">
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                        </span>
                      </button>
                    </div>
                  </div>
                  <Button type="submit" class="w-full"> Register </Button>
                  <div
                    class="relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t after:border-border"
                  >
                    <span
                      class="relative z-10 bg-background px-2 text-muted-foreground"
                    >
                      Or continue with
                    </span>
                  </div>
                  <div class="grid grid-cols-1 gap-4">
                    <GoogleLogin
                      :callback="oneTapGoogleLoginCallback"
                      :prompt="isOneTapPromptEnabled"
                    >
                      <Button variant="outline" class="w-full">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 24 24"
                        >
                          <path
                            d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
                            fill="currentColor"
                          />
                        </svg>
                        Continue with Google
                      </Button>
                    </GoogleLogin>
                  </div>
                  <div class="text-center text-sm">
                    Already have an account?
                    <a
                      href="#"
                      class="underline underline-offset-4"
                      @click.prevent="authType = 'LOGIN'"
                    >
                      Login
                    </a>
                  </div>
                </div>
              </form>
              <div class="relative hidden bg-muted md:block">
                <img
                  :src="authImageUrl"
                  alt="Image"
                  class="absolute inset-0 h-full w-full object-cover dark:brightness-[0.5]"
                />
              </div>
            </CardContent>
          </Card>

          <Card
            class="overflow-hidden w-full"
            v-motion
            :initial="{
              opacity: 0,
              y: authType === 'LOGIN' ? -40 : 40,
              scale: 0.1,
              rotateX: authType === 'LOGIN' ? '15deg' : '-15deg',
            }"
            :enter="{
              opacity: 1,
              y: 0,
              scale: 1,
              rotateX: '0deg',
              transition: {
                duration: 600,
                ease: [0.4, 0, 0.2, 1],
              },
            }"
            :leave="{
              opacity: 0,
              y: authType === 'LOGIN' ? 40 : -40,
              scale: 0.1,
              rotateX: authType === 'LOGIN' ? '-10deg' : '10deg',
              transition: {
                duration: 600,
                ease: [0.4, 0, 0.2, 1],
              },
            }"
            v-show="authType == 'LOGIN'"
          >
            <CardContent class="grid p-0 md:grid-cols-2">
              <form @submit.prevent="login" class="p-6 md:p-8">
                <div class="flex flex-col gap-6">
                  <div class="flex flex-col items-center text-center">
                    <h1 class="text-2xl font-bold">Welcome back</h1>
                    <p class="text-balance text-muted-foreground">
                      Login to your account
                    </p>
                  </div>
                  <div class="grid gap-2">
                    <Label for="email">Email</Label>
                    <Input
                      id="login-email"
                      type="email"
                      v-model="loginEmail"
                      placeholder="agent@ai.com"
                      required
                    />
                  </div>
                  <div class="grid gap-2">
                    <div class="flex items-center">
                      <Label for="password">Password</Label>
                      <a
                        @click.prevent="authType = 'FORGOT_PASSWORD'"
                        class="ml-auto cursor-pointer text-sm underline-offset-2 hover:underline"
                      >
                        Forgot your password?
                      </a>
                    </div>
                    <div class="relative">
                      <Input
                        id="login-password"
                        v-model="loginPassword"
                        :type="passwordVisibility.login ? 'text' : 'password'"
                        placeholder="*************"
                        class="pr-10"
                        required
                      />
                      <button 
                        type="button" 
                        class="absolute inset-y-0 right-0 flex items-center pr-3"
                        @click="togglePasswordVisibility('login')"
                      >
                        <span v-if="passwordVisibility.login" class="text-gray-500 hover:text-gray-700">
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"></path><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"></path><line x1="2" x2="22" y1="2" y2="22"></line></svg>
                        </span>
                        <span v-else class="text-gray-500 hover:text-gray-700">
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                        </span>
                      </button>
                    </div>
                  </div>
                  <Button type="submit" class="w-full"> Login </Button>
                  <div
                    class="relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t after:border-border"
                  >
                    <span
                      class="relative z-10 bg-background px-2 text-muted-foreground"
                    >
                      Or continue with
                    </span>
                  </div>
                  <div class="grid grid-cols-1 gap-4">
                    <GoogleLogin :callback="oneTapGoogleLoginCallback" prompt>
                      <Button variant="outline" class="w-full">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 24 24"
                        >
                          <path
                            d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
                            fill="currentColor"
                          />
                        </svg>
                        Continue with Google
                      </Button>
                    </GoogleLogin>
                  </div>
                  <div class="text-center text-sm">
                    Don&apos;t have an account?
                    <a
                      href="#"
                      class="underline underline-offset-4"
                      @click.prevent="authType = 'REGISTER'"
                    >
                      Sign up
                    </a>
                  </div>
                </div>
              </form>
              <div class="relative hidden bg-muted md:block">
                <img
                  :src="authImageUrl"
                  alt="Image"
                  class="absolute inset-0 h-full w-full object-cover dark:brightness-[0.5]"
                />
              </div>
            </CardContent>
          </Card>

          <Card
            class="overflow-hidden w-full"
            v-motion
            :initial="{
              opacity: 0,
              y: authType === 'LOGIN' ? -40 : 40,
              scale: 0.1,
              rotateX: authType === 'LOGIN' ? '15deg' : '-15deg',
            }"
            :enter="{
              opacity: 1,
              y: 0,
              scale: 1,
              rotateX: '0deg',
              transition: {
                duration: 600,
                ease: [0.4, 0, 0.2, 1],
              },
            }"
            :leave="{
              opacity: 0,
              y: authType === 'LOGIN' ? 40 : -40,
              scale: 0.1,
              rotateX: authType === 'LOGIN' ? '-10deg' : '10deg',
              transition: {
                duration: 600,
                ease: [0.4, 0, 0.2, 1],
              },
            }"
            v-show="authType == 'FORGOT_PASSWORD'"
          >
            <CardContent class="grid p-0 md:grid-cols-2">
              <form @submit.prevent="forgotPassword" class="p-6 md:p-8">
                <div class="flex flex-col gap-6">
                  <div class="flex flex-col items-center text-center">
                    <h1 class="text-2xl font-bold">Forgot your password?</h1>
                    <p class="text-balance text-muted-foreground">
                      Enter your email address to reset your password.
                    </p>
                  </div>
                  <div class="grid gap-2">
                    <Label for="email">Email</Label>
                    <Input
                      id="forgot-password-email"
                      type="email"
                      v-model="forgotPasswordEmail"
                      placeholder="agent@ai.com"
                      required
                    />
                  </div>
                  <Button type="submit" class="w-full">
                    Send reset link
                  </Button>
                </div>
              </form>
              <div class="relative hidden bg-muted md:block">
                <img
                  :src="authImageUrl"
                  alt="Image"
                  class="absolute inset-0 h-full w-full object-cover dark:brightness-[0.5]"
                />
              </div>
            </CardContent>
          </Card>
        </div>
      </transition>
    </div>
    <div
      class="text-balance text-center text-xs text-muted-foreground [&_a]:underline [&_a]:underline-offset-4 hover:[&_a]:text-primary"
    >
      By clicking continue, you agree to our
      <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
    </div>
  </div>
</template>

<script setup>
import authImageUrl from "@/assets/auth.svg";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
</script>

<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      isOneTapPromptEnabled: true,
      authType: "LOGIN",
      loginEmail: "",
      loginPassword: "",
      registerName: "",
      registerEmail: "",
      registerPassword: "",
      forgotPasswordEmail: "",
      passwordVisibility: {
        login: false,
        register: false,
        forgot: false
      },
    };
  },
  computed: {
    ...mapState(["TOASTER_DATA"]),
    ...mapState("auth", ["isLoading", "user"]),
  },
  watch: {
    "$route.params.type": {
      handler() {
        this.authType = this.$route.params.type?.toUpperCase() || "LOGIN";
      },
      immediate: true,
    },
    user: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.$router.push("/");
        }
      },
    },
  },
  mounted() {
    this.isOneTapPromptEnabled = location.href.includes("localhost")
      ? false
      : true;
  },
  methods: {
    togglePasswordVisibility(field) {
      this.passwordVisibility[field] = !this.passwordVisibility[field];
    },
    async oneTapGoogleLoginCallback(response) {
      console.log(response);
      // if (response.credential) {
      //   // decodeCredential will retrive the JWT payload from the credential
      //   const userData = decodeCredential(response.credential);
      //   console.log("Handle the userData", userData);
      // } else {
      // }
      if (response.credential) {
        await this.$store.dispatch("auth/loginViaGoogle", {
          idToken: response.credential,
        });
        await this.$store.dispatch("auth/getUserProfile");
      } else {
        await this.$store.dispatch("auth/loginViaGoogle", {
          code: response.code,
        });
        await this.$store.dispatch("auth/getUserProfile");
      }
    },
    async login() {
      try {
        if (this.loginEmail && this.loginPassword) {
          await this.$store.dispatch("auth/login", {
            email: this.loginEmail,
            password: this.loginPassword,
          });

          await this.$store.dispatch("auth/getUserProfile");
        }
      } catch (e) {
        console.error(e);
      }
    },
    async register() {
      try {
        if (this.registerName && this.registerEmail && this.registerPassword) {
          await this.$store.dispatch("auth/register", {
            name: this.registerName,
            email: this.registerEmail,
            password: this.registerPassword,
          });

          await this.$store.dispatch("auth/getUserProfile");
        }
      } catch (e) {
        console.error(e);
      }
    },
    async forgotPassword() {
      try {
        if (this.forgotPasswordEmail) {
          await this.$store.dispatch("auth/forgotPassword", {
            email: this.forgotPasswordEmail,
          });
        }
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>
