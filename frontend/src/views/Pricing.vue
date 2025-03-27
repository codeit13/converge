<template>
  <div class="pricing-container max-w-6xl mx-auto px-4 py-8 sm:py-12">
    <!-- Page Header -->
    <div class="text-center mb-8 sm:mb-12">
      <h1 class="text-3xl sm:text-4xl font-bold mb-3">Subscription Plans</h1>
      <p class="text-muted-foreground max-w-2xl mx-auto">
        Power your sales and marketing with AI automation. Choose the plan that
        fits your business needs.
      </p>
    </div>

    <!-- Loading State - Skeleton Loader -->
    <div v-if="isLoading" class="space-y-6">
      <div class="flex justify-center items-center gap-3 mb-4">
        <Loader2 class="h-6 w-6 animate-spin text-primary" />
        <span>Loading subscription data...</span>
      </div>
      <div class="grid md:grid-cols-3 gap-6">
        <div
          v-for="i in 3"
          :key="i"
          class="h-[400px] rounded-xl border bg-card/30 animate-pulse"
        ></div>
      </div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="max-w-md mx-auto text-center py-8 px-4 border rounded-xl bg-card"
    >
      <AlertCircle class="h-10 w-10 text-destructive mx-auto mb-4" />
      <h3 class="text-xl font-semibold mb-2">Unable to Load Plans</h3>
      <p class="text-muted-foreground mb-6">{{ error }}</p>
      <Button @click="retryLoading" class="gap-2">
        <RefreshCcw class="h-4 w-4" />
        Try Again
      </Button>
    </div>

    <!-- Current Subscription Card -->
    <div
      v-else-if="
        !isEmpty(subscriptionStatus) && subscriptionStatus.status !== 'none'
      "
      class="mb-12"
    >
      <div class="max-w-3xl mx-auto rounded-xl border bg-card p-6 sm:p-8">
        <div
          class="flex flex-col md:flex-row md:justify-between md:items-start gap-6"
        >
          <!-- Subscription Info -->
          <div class="space-y-4">
            <div class="flex items-center gap-2">
              <Badge variant="outline" class="px-3 py-1 text-sm">
                Active Subscription
              </Badge>
              <Badge
                v-if="subscriptionStatus.currentPlan?.popular"
                class="bg-primary text-primary-foreground"
              >
                Popular Plan
              </Badge>
            </div>

            <h3 class="text-2xl font-bold">
              {{ subscriptionStatus.currentPlan?.name || "Current Plan" }}
            </h3>

            <p class="text-muted-foreground">
              <span class="font-medium text-foreground text-xl">
                {{ subscriptionStatus.currentPlan?.amount }}
                {{ subscriptionStatus.currentPlan?.currency }}
              </span>
              <span v-if="subscriptionStatus.currentPlan?.interval">
                /{{ subscriptionStatus.currentPlan.interval }}
              </span>
            </p>

            <!-- Plan Features -->
            <div
              v-if="subscriptionStatus.currentPlan?.features?.length"
              class="pt-2"
            >
              <p class="text-sm font-medium mb-2">Plan Features:</p>
              <ul class="space-y-2">
                <li
                  v-for="feature in subscriptionStatus.currentPlan.features.slice(
                    0,
                    3
                  )"
                  :key="feature"
                  class="flex items-center gap-2 text-sm"
                >
                  <CheckCircle2 class="h-4 w-4 text-primary" />
                  <span>{{ feature }}</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Usage and Actions -->
          <div class="space-y-6 sm:min-w-[200px]">
            <!-- Usage Meter -->
            <div v-if="subscriptionStatus.usage" class="space-y-2">
              <div class="flex justify-between text-sm mb-1">
                <p class="font-medium">Usage</p>
                <p class="text-muted-foreground">
                  {{ Math.round(getUsagePercentage()) }}% used
                </p>
              </div>
              <div class="h-2 w-full bg-muted rounded-full overflow-hidden">
                <div
                  class="h-full transition-all"
                  :class="{
                    'bg-green-500': getUsagePercentage() < 70,
                    'bg-amber-500':
                      getUsagePercentage() >= 70 && getUsagePercentage() < 90,
                    'bg-red-500': getUsagePercentage() >= 90,
                  }"
                  :style="{ width: `${getUsagePercentage()}%` }"
                ></div>
              </div>
              <p class="text-xs text-muted-foreground">
                {{ formatUsage(subscriptionStatus.usage) }}
              </p>
            </div>

            <!-- Action Buttons -->
            <div class="flex flex-col sm:flex-row gap-2 mt-4">
              <Button
                variant="outline"
                class="w-full sm:w-auto"
                @click="viewPaymentHistory"
              >
                <ClipboardList class="h-4 w-4 mr-2" />
                Payment History
              </Button>
              <Button class="w-full sm:w-auto" @click="scrollToPlans">
                <ArrowUpCircle class="h-4 w-4 mr-2" />
                Upgrade
              </Button>
            </div>

            <!-- Cancel button for active subscriptions -->
            <!-- <Button
              v-if="canCancel"
              variant="outline"
              size="sm"
              @click="showCancelDialog = true"
              class="w-full text-destructive hover:text-destructive hover:bg-destructive/10 border-destructive/20"
            >
              <XCircle class="h-4 w-4 mr-2" />
              Cancel Subscription
            </Button> -->
          </div>
        </div>
      </div>
    </div>

    <!-- Plans Grid -->
    <div
      id="plans-section"
      class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8"
    >
      <div
        v-for="plan in sortedPlans"
        :key="plan._id"
        class="relative rounded-xl border bg-card shadow-sm transition-all hover:shadow-md"
        :class="{
          'border-primary ring-1 ring-primary/20': plan.isPopular,
        }"
      >
        <!-- Popular Badge -->
        <div
          v-if="plan.isPopular"
          class="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-primary text-primary-foreground text-sm font-medium rounded-full"
        >
          Most Popular
        </div>

        <!-- Current Plan Badge -->
        <div
          v-if="isCurrentPlan(plan)"
          class="absolute -top-3 right-4 px-3 py-1 bg-green-500 text-white text-sm font-medium rounded-full"
        >
          Current Plan
        </div>

        <div class="p-6">
          <h3 class="text-xl font-bold">{{ plan.displayName || plan.name }}</h3>
          <p v-if="plan.description" class="text-sm text-muted-foreground mt-1">
            {{ plan.description }}
          </p>
          <div class="mt-3 flex items-baseline">
            <span class="text-3xl font-bold">
              {{ getPlanPrice(plan) }} {{ getPlanCurrency(plan) }}
            </span>
            <span class="ml-1 text-muted-foreground"
              >/{{ getPlanInterval(plan) }}</span
            >
          </div>

          <ul class="mt-6 space-y-3">
            <!-- Handle string features (backward compatibility) -->
            <li
              v-for="feature in getFeaturesList(plan)"
              :key="typeof feature === 'string' ? feature : feature._id"
              class="flex items-start gap-2 text-sm"
            >
              <CheckCircle2 class="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
              <div>
                <span v-if="typeof feature === 'string'">{{ feature }}</span>
                <template v-else>
                  <span>{{ feature.name }}</span>
                  <p
                    v-if="feature.description"
                    class="text-xs text-muted-foreground"
                  >
                    {{ feature.description }}
                  </p>
                </template>
              </div>
            </li>
          </ul>

          <Button
            :variant="plan.popular ? 'default' : 'outline'"
            class="w-full mt-6"
            size="lg"
            :disabled="processingPlans[plan._id] || isCurrentPlan(plan)"
            @click="handlePurchase(plan)"
          >
            <Loader2
              v-if="processingPlans[plan._id]"
              class="mr-2 h-4 w-4 animate-spin"
            />
            {{ getPlanButtonText(plan) }}
          </Button>
        </div>
      </div>
    </div>

    <!-- Cancel Subscription Dialog -->
    <Dialog :open="showCancelDialog" @update:open="showCancelDialog = $event">
      <DialogContent class="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Cancel Subscription</DialogTitle>
          <DialogDescription>
            Are you sure you want to cancel your subscription? You'll continue
            to have access until the end of your current billing period.
          </DialogDescription>
        </DialogHeader>
        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <Label for="reason">Reason for cancellation</Label>
            <Select v-model="cancelReason">
              <SelectTrigger id="reason">
                <SelectValue placeholder="Select a reason" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="too_expensive">Too expensive</SelectItem>
                <SelectItem value="not_using">Not using the service</SelectItem>
                <SelectItem value="missing_features"
                  >Missing features</SelectItem
                >
                <SelectItem value="found_alternative"
                  >Found an alternative</SelectItem
                >
                <SelectItem value="other">Other reason</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div v-if="cancelReason === 'other'" class="space-y-2">
            <Label for="comment">Please specify</Label>
            <Textarea
              id="comment"
              v-model="cancelComment"
              placeholder="Tell us more..."
            />
          </div>
        </div>
        <DialogFooter class="flex sm:justify-between">
          <Button variant="ghost" @click="showCancelDialog = false">
            Never mind
          </Button>
          <Button
            variant="destructive"
            @click="handleCancelSubscription"
            :disabled="cancelInProgress"
          >
            <Loader2
              v-if="cancelInProgress"
              class="mr-2 h-4 w-4 animate-spin"
            />
            {{ cancelInProgress ? "Processing..." : "Cancel Subscription" }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Payment Success Dialog -->
    <Dialog :open="showSuccessDialog" @update:open="showSuccessDialog = $event">
      <DialogContent class="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Payment Successful!</DialogTitle>
          <DialogDescription>
            Your subscription has been successfully activated. You now have
            access to all features of your selected plan.
          </DialogDescription>
        </DialogHeader>
        <div class="py-4">
          <div class="rounded-lg bg-muted p-4 flex items-center gap-3">
            <div class="p-2 rounded-full bg-green-100">
              <CheckCircle2 class="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p class="font-medium">
                {{ lastSuccessfulPlan?.name || "Your new plan" }} activated
              </p>
              <p class="text-sm text-muted-foreground">
                Valid until {{ formatExpiryDate() }}
              </p>
            </div>
          </div>
        </div>
        <DialogFooter>
          <Button @click="goToDashboard">Go to Dashboard</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Refund Request Dialog -->
    <Dialog :open="showRefundDialog" @update:open="showRefundDialog = $event">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Request Refund</DialogTitle>
          <DialogDescription>
            Please provide details for your refund request. Refunds are
            processed according to our refund policy.
          </DialogDescription>
        </DialogHeader>
        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <Label for="payment">Payment</Label>
            <Select v-model="refundPaymentId">
              <SelectTrigger id="payment">
                <SelectValue placeholder="Select payment" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem
                  v-for="payment in refundablePayments"
                  :key="payment.id"
                  :value="payment.id"
                >
                  {{ payment.amount }} {{ payment.currency }} -
                  {{ formatDate(payment.createdAt) }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="space-y-2">
            <Label for="refund-reason">Reason for refund</Label>
            <Textarea
              id="refund-reason"
              v-model="refundReason"
              placeholder="Please explain why you're requesting a refund"
            />
          </div>
        </div>
        <DialogFooter>
          <Button variant="ghost" @click="showRefundDialog = false">
            Cancel
          </Button>
          <Button
            @click="handleRefundRequest"
            :disabled="refundInProgress || !refundPaymentId || !refundReason"
          >
            <Loader2
              v-if="refundInProgress"
              class="mr-2 h-4 w-4 animate-spin"
            />
            {{ refundInProgress ? "Processing..." : "Submit Request" }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
    <!-- Success Dialog after Payment -->
    <Dialog :open="showSuccessDialog" @update:open="showSuccessDialog = $event">
      <DialogContent class="sm:max-w-md text-center">
        <DialogHeader>
          <DialogTitle class="text-center text-2xl"
            >Payment Successful!</DialogTitle
          >
          <DialogDescription class="text-center">
            Thank you for subscribing to our service.
          </DialogDescription>
        </DialogHeader>

        <div class="my-6 flex flex-col items-center space-y-4">
          <div
            class="h-16 w-16 rounded-full bg-green-100 flex items-center justify-center"
          >
            <CheckCircle2 class="h-10 w-10 text-green-600" />
          </div>

          <div class="space-y-2">
            <h3 class="text-lg font-semibold">
              {{ lastSuccessfulPlan?.name }}
            </h3>
            <p class="text-muted-foreground">
              {{ lastSuccessfulPlan?.pricing[0].amount }}
              {{ lastSuccessfulPlan?.pricing[0].currency }}/{{
                lastSuccessfulPlan?.pricing[0].interval || "month"
              }}
            </p>
          </div>
        </div>

        <div class="rounded-lg border bg-muted/50 p-4 my-4 text-sm">
          <p class="mb-2 font-medium">Your subscription includes:</p>
          <ul class="space-y-1 pl-2">
            <li
              v-for="(feature, i) in lastSuccessfulPlan?.features?.slice(0, 3)"
              :key="i"
              class="flex items-center gap-2"
            >
              <CheckCircle2 class="h-3 w-3 text-green-600 flex-shrink-0" />
              <span>{{ feature.name }}</span>
            </li>
          </ul>
        </div>

        <DialogFooter>
          <Button class="w-full" @click="goToDashboard">
            Go to Dashboard
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup>
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  CheckCircle2,
  Loader2,
  AlertCircle,
  ArrowUpCircle,
  RefreshCcw,
  XCircle,
  ClipboardList,
} from "lucide-vue-next";
</script>

<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      processingPlans: {}, // Track loading state per plan
      selectedPlan: null,

      showCancelDialog: false,
      showSuccessDialog: false,
      showRefundDialog: false,
      cancelReason: "",
      cancelComment: "",
      cancelInProgress: false,
      refundPaymentId: "",
      refundReason: "",
      refundInProgress: false,
      lastSuccessfulPlan: null,
      razorpayInstance: null,
    };
  },
  computed: {
    ...mapState("payments", [
      "plans",
      "isLoading",
      "error",
      "subscriptionStatus",
      "paymentHistory",
    ]),
    ...mapState("auth", ["user", "currentProject"]),
    sortedPlans() {
      if (!this.plans || !Array.isArray(this.plans)) return [];
      return [...this.plans].sort((a, b) => {
        // Sort by position first if available
        if (a.position !== undefined && b.position !== undefined) {
          return a.position - b.position;
        }
        // Otherwise sort by price
        const priceA = this.getPlanPrice(a) || 0;
        const priceB = this.getPlanPrice(b) || 0;
        return priceA - priceB;
      });
    },
    canCancel() {
      return (
        this.subscriptionStatus?.status !== "none" &&
        this.subscriptionStatus?.currentPlan !== null &&
        this.subscriptionStatus?.currentPlan?.cancellable !== false
      );
    },
    refundablePayments() {
      if (!this.paymentHistory?.payments) return [];

      const now = new Date();
      return this.paymentHistory.payments.filter((payment) => {
        // Only show successful payments from the last 30 days that haven't been refunded
        const paymentDate = new Date(payment.createdAt);
        const daysDiff = Math.floor(
          (now - paymentDate) / (1000 * 60 * 60 * 24)
        );
        return (
          payment.status === "success" && !payment.refunded && daysDiff <= 30
        );
      });
    },
  },
  methods: {
    // Helper methods
    isEmpty(obj) {
      return !obj || Object.keys(obj).length === 0;
    },

    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      return new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      }).format(date);
    },

    formatExpiryDate() {
      const date = new Date();
      // Assuming monthly subscription by default
      date.setMonth(date.getMonth() + 1);
      return this.formatDate(date);
    },

    getUsagePercentage() {
      if (
        !this.subscriptionStatus?.usage?.current ||
        !this.subscriptionStatus?.usage?.limit
      ) {
        return 0;
      }
      return Math.min(
        (this.subscriptionStatus.usage.current /
          this.subscriptionStatus.usage.limit) *
          100,
        100
      );
    },

    formatUsage(usage) {
      if (!usage?.current || !usage?.limit) return "No usage data";
      return `${usage.current.toLocaleString()} / ${usage.limit.toLocaleString()} ${
        usage.unit || "credits"
      }`;
    },

    // Status and UI interaction methods
    isCurrentPlan(plan) {
      if (!this.subscriptionStatus?.currentPlan) return false;
      return (
        this.subscriptionStatus.currentPlan._id === plan._id ||
        this.subscriptionStatus.currentPlan.name === plan.name
      );
    },

    getPlanPrice(plan) {
      if (!plan?.pricing || !plan.pricing.length) return 0;
      return plan.pricing[0].amount;
    },

    getPlanCurrency(plan) {
      if (!plan?.pricing || !plan.pricing.length) return "";
      return plan.pricing[0].currency;
    },

    getPlanInterval(plan) {
      if (!plan?.pricing || !plan.pricing.length) return "month";
      return plan.pricing[0].interval;
    },

    getFeaturesList(plan) {
      if (!plan?.features) return [];

      // If features is an array of strings (old format)
      if (
        Array.isArray(plan.features) &&
        plan.features.length > 0 &&
        typeof plan.features[0] === "string"
      ) {
        return plan.features;
      }

      // If features is an array of objects (new format)
      if (Array.isArray(plan.features)) {
        return plan.features.filter(
          (feature) => feature && feature.included !== false
        );
      }

      return [];
    },

    getPlanButtonText(plan) {
      if (this.processingPlans[plan._id]) {
        return "Processing...";
      }
      if (this.isCurrentPlan(plan)) {
        return "Current Plan";
      }
      if (plan.free) {
        return "Get Started";
      }
      return "Subscribe";
    },

    scrollToPlans() {
      const plansSection = document.getElementById("plans-section");
      if (plansSection) {
        plansSection.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    },

    async retryLoading() {
      this.$store.commit("payments/SET_ERROR", null);
      await this.$store.dispatch("payments/fetchPlans");
      if (this.user) {
        await this.$store.dispatch("payments/getSubscriptionStatus");
      }
    },

    async viewPaymentHistory() {
      await this.$store.dispatch("payments/getPaymentHistory");
      this.$router.push("/payment-history");
    },

    async handleRefundRequestClick() {
      // First load payment history if not already loaded
      if (!this.paymentHistory?.payments?.length) {
        await this.$store.dispatch("payments/getPaymentHistory");
        this.showRefundDialog = true;
      } else {
        this.showRefundDialog = true;
      }
    },

    async handleRefundRequest() {
      if (!this.refundPaymentId || !this.refundReason) {
        this.$store.dispatch("auth/showNotification", {
          type: "warning",
          message: "Please complete all fields",
        });
        return;
      }

      try {
        this.refundInProgress = true;
        await this.$store.dispatch("payments/initiateRefund", {
          paymentId: this.refundPaymentId,
          reason: this.refundReason,
        });

        // Update payment history after refund
        await this.$store.dispatch("payments/getPaymentHistory");

        this.$store.dispatch("auth/showNotification", {
          type: "success",
          message: "Refund request submitted successfully",
        });

        this.showRefundDialog = false;
        this.refundPaymentId = "";
        this.refundReason = "";
      } catch (error) {
        this.$store.dispatch("auth/showNotification", {
          type: "error",
          message: error?.response?.data?.message || "Failed to process refund",
        });
      } finally {
        this.refundInProgress = false;
      }
    },

    async handleCancelSubscription() {
      if (!this.cancelReason) {
        this.$store.dispatch("auth/showNotification", {
          type: "warning",
          message: "Please select a reason for cancellation",
        });
        return;
      }

      this.cancelInProgress = true;

      try {
        // Implement API call to cancel subscription when available
        // For now, just show success and update local state
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // Update subscription status
        await this.$store.dispatch("payments/getSubscriptionStatus");

        this.$store.dispatch("auth/showNotification", {
          type: "success",
          message: "Subscription cancelled successfully",
        });

        this.showCancelDialog = false;
        this.cancelReason = "";
        this.cancelComment = "";
      } catch (error) {
        // this.$store.dispatch("auth/showNotification", {
        //   type: "error",
        //   message:
        //     error?.response?.data?.message || "Failed to cancel subscription",
        // });
      } finally {
        this.cancelInProgress = false;
      }
    },

    goToDashboard() {
      this.showSuccessDialog = false;
      this.$router.push("/");
    },

    // Main purchase handler
    async handlePurchase(plan) {
      // Check if user is logged in
      if (!this.user) {
        this.$router.push("/auth/login");
        return;
      }

      // Check if already subscribed to this plan
      if (this.isCurrentPlan(plan)) {
        this.$store.dispatch("auth/showNotification", {
          type: "info",
          message: "You are already subscribed to this plan",
        });
        return;
      }

      // Set loading state for this specific plan
      this.processingPlans = { ...this.processingPlans, [plan._id]: true };
      this.selectedPlan = plan;

      try {
        // Check if Razorpay is loaded
        if (!window.Razorpay) {
          throw new Error(
            "Payment gateway not loaded. Please refresh the page."
          );
        }

        // Create payment
        const res = await this.$store.dispatch("payments/createPayment", {
          planId: plan._id,
          gateway: "razorpay", // or "stripe" based on configuration
        });

        // Validate payment creation response
        if (!res?.status || !res?.data?.payment) return;

        const payment = res.data.payment;
        const projectName = this.currentProject?.name || "Sales AI";

        // Validate required payment data
        if (
          !payment.amount ||
          !payment.currency ||
          !payment?.gateway?.orderId
        ) {
          throw new Error("Invalid payment data received from server");
        }

        // Initialize Razorpay options
        const options = {
          key: import.meta.env.VITE_RAZORPAY_KEY_ID,
          amount: payment.amount,
          currency: payment.currency,
          name: projectName,
          description: `${plan.name} Plan - ${this.getPlanInterval(plan)}`,
          order_id: payment.gateway.orderId,
          handler: async (response) => {
            try {
              // Validate response
              if (
                !response.razorpay_payment_id ||
                !response.razorpay_order_id ||
                !response.razorpay_signature
              ) {
                throw new Error("Invalid payment response received");
              }

              // Verify payment
              await this.$store.dispatch("payments/verifyPayment", {
                data: response,
                paymentId: payment.paymentId,
              });

              // Get updated subscription status
              await this.$store.dispatch("payments/getSubscriptionStatus");

              // Set last successful plan for the success dialog
              this.lastSuccessfulPlan = plan;
              this.showSuccessDialog = true;

              // Show success notification
              this.$store.dispatch("auth/showNotification", {
                type: "success",
                message: "Payment successful! Your subscription is now active.",
              });
            } catch (e) {
              this.$store.dispatch("auth/showNotification", {
                type: "error",
                message:
                  e?.response?.data?.message ||
                  e.message ||
                  "Payment verification failed",
              });
            } finally {
              // Clear loading state for this plan
              this.processingPlans = {
                ...this.processingPlans,
                [plan._id]: false,
              };
              this.selectedPlan = null;

              // Cleanup Razorpay instance
              if (this.razorpayInstance) {
                this.razorpayInstance = null;
              }
            }
          },
          modal: {
            ondismiss: () => {
              // Clear loading state when modal is dismissed
              this.processingPlans = {
                ...this.processingPlans,
                [plan._id]: false,
              };
              this.selectedPlan = null;

              // Show info notification
              this.$store.dispatch("auth/showNotification", {
                type: "info",
                message: "Payment cancelled",
              });
            },
          },
          prefill: {
            name: this.user.name,
            email: this.user.email,
            contact: this.user.phone || "",
          },
          theme: {
            color: "hsl(var(--primary))",
          },
        };

        // Create and open Razorpay instance
        this.razorpayInstance = new window.Razorpay(options);
        this.razorpayInstance.open();
      } catch (e) {
        // Handle errors
        this.$store.dispatch("auth/showNotification", {
          type: "error",
          message:
            e?.response?.data?.message ||
            e.message ||
            "Failed to create payment",
        });

        // Clear loading state for this plan
        this.processingPlans = { ...this.processingPlans, [plan._id]: false };
        this.selectedPlan = null;
      }
    },
  },
  async mounted() {
    try {
      // Initialize empty processing plans object
      this.processingPlans = {};

      // Load subscription plans
      await this.$store.dispatch("payments/fetchPlans");

      // If user is logged in, load subscription status
      if (this.user) {
        await this.$store.dispatch("payments/getPaymentHistory");
        await this.$store.dispatch("payments/getSubscriptionStatus");
      }

      // Check if Razorpay script is already loaded
      if (!window.Razorpay) {
        // Load Razorpay script dynamically
        const script = document.createElement("script");
        script.src = "https://checkout.razorpay.com/v1/checkout.js";
        script.async = true;
        script.onerror = () => {
          this.$store.dispatch("auth/showNotification", {
            type: "error",
            message: "Failed to load payment gateway. Please refresh the page.",
          });
        };
        document.body.appendChild(script);
      }
    } catch (error) {
      console.error("Error loading pricing data:", error);
      this.$store.dispatch("auth/showNotification", {
        type: "error",
        message: "Failed to load subscription data. Please try again later.",
      });
    }
  },
};
</script>

<style scoped>
.pricing-container {
  width: 100%;
  display: block;
}
</style>
