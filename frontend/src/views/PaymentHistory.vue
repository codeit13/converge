<template>
  <div class="container mx-auto px-4 py-16">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold">Payment History</h1>
        <p class="text-muted-foreground mt-2">
          View all your past transactions
        </p>
      </div>
      <Button variant="outline" @click="$router.push('/pricing')">
        <ArrowLeft class="h-4 w-4 mr-2" />
        Back to Plans
      </Button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <Loader2 class="h-8 w-8 animate-spin text-primary" />
      <span class="ml-3 text-lg">Loading payment history...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="max-w-lg mx-auto text-center py-12">
      <AlertCircle class="h-12 w-12 text-destructive mx-auto mb-4" />
      <h3 class="text-lg font-semibold mb-2">Failed to Load History</h3>
      <p class="text-muted-foreground mb-6">{{ error }}</p>
      <Button @click="retryLoading">Try Again</Button>
    </div>

    <!-- No Payments -->
    <div
      v-else-if="!filteredPayments.length"
      class="max-w-lg mx-auto text-center py-12"
    >
      <Receipt class="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
      <h3 class="text-lg font-semibold mb-2">No Payment History</h3>
      <p class="text-muted-foreground mb-6">
        You haven't made any payments yet.
      </p>
      <Button @click="$router.push('/pricing')">View Plans</Button>
    </div>

    <!-- Filter Controls -->
    <div
      v-else
      class="mb-6 p-4 bg-muted/40 rounded-lg"
    >
      <div class="flex flex-wrap gap-4 mb-4">
        <div class="w-full md:w-auto">
          <label class="text-sm font-medium mb-1 block">Status</label>
          <select
            v-model="filters.status"
            class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
          >
            <option value="">All Statuses</option>
            <option value="completed">Completed</option>
            <option value="pending">Pending</option>
            <option value="failed">Failed</option>
          </select>
        </div>

        <div class="w-full md:w-auto">
          <label class="text-sm font-medium mb-1 block">Payment Type</label>
          <select
            v-model="filters.type"
            class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
          >
            <option value="">All Types</option>
            <option value="subscription">Subscription</option>
            <option value="onetime">One-time</option>
          </select>
        </div>

        <div class="w-full md:w-auto">
          <label class="text-sm font-medium mb-1 block">Gateway</label>
          <select
            v-model="filters.gateway"
            class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
          >
            <option value="">All Gateways</option>
            <option value="razorpay">Razorpay</option>
            <option value="stripe">Stripe</option>
          </select>
        </div>

        <div class="w-full md:w-auto">
          <label class="text-sm font-medium mb-1 block">Start Date</label>
          <input
            type="date"
            v-model="filters.startDate"
            class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
          />
        </div>

        <div class="w-full md:w-auto">
          <label class="text-sm font-medium mb-1 block">End Date</label>
          <input
            type="date"
            v-model="filters.endDate"
            class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
          />
        </div>

        <div class="w-full md:w-auto">
          <label class="text-sm font-medium mb-1 block">Sort By</label>
          <select
            v-model="filters.sortBy"
            class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
          >
            <option value="">Default</option>
            <option value="date:desc">Date (Newest)</option>
            <option value="date:asc">Date (Oldest)</option>
            <option value="amount:desc">Amount (High-Low)</option>
            <option value="amount:asc">Amount (Low-High)</option>
          </select>
        </div>
      </div>

      <div class="flex justify-end gap-2">
        <Button variant="outline" @click="resetFilters">Reset Filters</Button>
        <Button @click="applyFilters">Apply Filters</Button>
      </div>
    </div>

    <!-- Payment History Cards -->
    <div v-if="filteredPayments.length" class="space-y-6">
      <Card v-for="payment in filteredPayments" :key="payment.id" class="overflow-hidden">
        <CardHeader class="pb-2">
          <div class="flex justify-between items-start">
            <div>
              <CardTitle class="flex items-center gap-2">
                {{ payment.metadata?.planName || "Payment" }}
                <Badge
                  :variant="getStatusVariant(payment.status)"
                >
                  {{ payment.status }}
                </Badge>
              </CardTitle>
              <CardDescription>
                {{ formatDate(payment.createdAt) }}
              </CardDescription>
            </div>
            <div class="text-right">
              <div class="text-xl font-bold">{{ payment.amount }} {{ payment.currency }}</div>
              <div class="text-sm text-muted-foreground">{{ payment.type }}</div>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs default-value="details" class="w-full">
            <TabsList class="grid w-full grid-cols-4">
              <TabsTrigger value="details">Details</TabsTrigger>
              <TabsTrigger value="gateway">Gateway</TabsTrigger>
              <TabsTrigger value="subscription" :disabled="!payment.subscription">Subscription</TabsTrigger>
              <TabsTrigger value="plan" :disabled="!payment.planData && !payment.metadata">Plan</TabsTrigger>
            </TabsList>
            
            <!-- Details Tab -->
            <TabsContent value="details">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Payment ID</h4>
                  <p class="font-mono text-sm">{{ payment.paymentId }}</p>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Type</h4>
                  <p>{{ payment.type }}</p>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Created</h4>
                  <p>{{ formatDate(payment.createdAt, true) }}</p>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Updated</h4>
                  <p>{{ formatDate(payment.updatedAt, true) }}</p>
                </div>
                <div v-if="payment.requestData">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">IP Address</h4>
                  <p>{{ payment.requestData.ipAddress }}</p>
                </div>
                <div v-if="payment.failureReason && payment.status === 'failed'">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Failure Reason</h4>
                  <p class="text-destructive">{{ payment.failureReason.message || "Unknown error" }}</p>
                </div>
              </div>
            </TabsContent>
            
            <!-- Gateway Tab -->
            <TabsContent value="gateway">
              <div v-if="payment.gateway" class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Gateway</h4>
                  <p class="capitalize">{{ payment.gateway.name }}</p>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Order ID</h4>
                  <p class="font-mono text-sm">{{ payment.gateway.orderId }}</p>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Payment ID</h4>
                  <p class="font-mono text-sm">{{ payment.gateway.paymentId }}</p>
                </div>
                <div v-if="payment.gateway.metadata">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Method</h4>
                  <p class="capitalize">{{ payment.gateway.metadata.method || "N/A" }}</p>
                </div>
                <div v-if="payment.gateway.metadata && payment.gateway.metadata.bank">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Bank</h4>
                  <p>{{ payment.gateway.metadata.bank }}</p>
                </div>
                <div v-if="payment.gateway.metadata && payment.gateway.metadata.email">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Email</h4>
                  <p>{{ payment.gateway.metadata.email }}</p>
                </div>
                <div v-if="payment.gateway.metadata && payment.gateway.metadata.contact">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Contact</h4>
                  <p>{{ payment.gateway.metadata.contact }}</p>
                </div>
                <div v-if="payment.gateway.metadata && payment.gateway.metadata.status">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Gateway Status</h4>
                  <Badge :variant="payment.gateway.metadata.status === 'captured' ? 'success' : 'secondary'">
                    {{ payment.gateway.metadata.status }}
                  </Badge>
                </div>
              </div>
              <div v-else class="py-4 text-center text-muted-foreground">
                No gateway information available
              </div>
            </TabsContent>
            
            <!-- Subscription Tab -->
            <TabsContent value="subscription">
              <div v-if="payment.subscription" class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Status</h4>
                  <Badge :variant="payment.subscription.status === 'active' ? 'success' : 'secondary'">
                    {{ payment.subscription.status }}
                  </Badge>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Auto Renew</h4>
                  <Badge variant="outline">
                    {{ payment.subscription.autoRenew ? 'Yes' : 'No' }}
                  </Badge>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Start Date</h4>
                  <p>{{ formatDate(payment.subscription.startDate) }}</p>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">End Date</h4>
                  <p>{{ formatDate(payment.subscription.endDate) }}</p>
                </div>
                <div v-if="payment.subscription.trialDays">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Trial Period</h4>
                  <p>{{ payment.subscription.trialDays }} days</p>
                </div>
                <div v-if="payment.subscription.cancelledAt">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Cancelled On</h4>
                  <p>{{ formatDate(payment.subscription.cancelledAt) }}</p>
                </div>
              </div>
              <div v-else class="py-4 text-center text-muted-foreground">
                No subscription information available
              </div>
            </TabsContent>
            
            <!-- Plan Tab -->
            <TabsContent value="plan">
              <div v-if="payment.metadata" class="grid grid-cols-1 gap-4 mt-4">
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Plan Name</h4>
                  <p>{{ payment.metadata.planName || "N/A" }}</p>
                </div>
                <div v-if="payment.metadata.planDescription">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Description</h4>
                  <p>{{ payment.metadata.planDescription }}</p>
                </div>
                <div v-if="payment.metadata.pricingInterval">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Billing Cycle</h4>
                  <p class="capitalize">{{ payment.metadata.pricingInterval }}</p>
                </div>
                <div v-if="payment.metadata.features && payment.metadata.features.length">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Features</h4>
                  <ul class="list-disc pl-5 space-y-1">
                    <li v-for="feature in payment.metadata.features" :key="feature._id" 
                        :class="{'text-muted-foreground': !feature.included}">
                      {{ feature.name }}
                      <span v-if="feature.description" class="text-xs text-muted-foreground">
                        - {{ feature.description }}
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
              <div v-else-if="payment.planData" class="grid grid-cols-1 gap-4 mt-4">
                <div>
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Plan ID</h4>
                  <p class="font-mono text-sm">{{ payment.plan }}</p>
                </div>
                <div v-if="payment.planData.name">
                  <h4 class="text-sm font-medium text-muted-foreground mb-1">Plan Name</h4>
                  <p>{{ payment.planData.name }}</p>
                </div>
              </div>
              <div v-else class="py-4 text-center text-muted-foreground">
                No plan information available
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
        
        <CardFooter class="flex justify-between border-t pt-4">
          <div class="text-sm text-muted-foreground">
            ID: <span class="font-mono">{{ payment.id }}</span>
          </div>
          
          <div class="flex gap-2">
            <Button 
              v-if="payment.status === 'pending'" 
              variant="default" 
              size="sm"
              @click="continuePayment(payment)"
            >
              <CreditCard class="h-4 w-4 mr-2" />
              Continue Payment
            </Button>
            <Button 
              variant="outline" 
              size="sm"
              @click="viewReceipt(payment)"
            >
              <Receipt class="h-4 w-4 mr-2" />
              View Receipt
            </Button>
          </div>
        </CardFooter>
      </Card>
      
      <!-- Pagination Controls -->
      <div class="flex items-center justify-between py-4">
        <div class="flex items-center gap-2">
          <span class="text-sm text-muted-foreground">
            Showing {{ Math.min(pagination.limit, pagination.totalResults) }} of
            {{ pagination.totalResults }} items
          </span>
          <select
            v-model="filters.limit"
            class="h-9 w-16 rounded-md border border-input bg-background px-2 text-sm"
            @change="applyFilters"
          >
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
          </select>
        </div>

        <div class="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            :disabled="pagination.page <= 1"
            @click="prevPage"
          >
            <ChevronLeft class="h-4 w-4" />
            Previous
          </Button>
          <span class="text-sm">
            Page {{ pagination.page }} of {{ pagination.totalPages }}
          </span>
          <Button
            variant="outline"
            size="sm"
            :disabled="pagination.page >= pagination.totalPages"
            @click="nextPage"
          >
            Next
            <ChevronRight class="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import { 
  ArrowLeft, 
  Loader2, 
  AlertCircle, 
  Receipt, 
  CreditCard,
  ChevronLeft,
  ChevronRight,
} from "lucide-vue-next";
</script>

<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      filters: {
        status: "",
        type: "",
        gateway: "",
        startDate: "",
        endDate: "",
        sortBy: "",
        limit: 10,
        page: 1,
      },
    };
  },
  computed: {
    ...mapState("payments", ["paymentHistory", "isLoading", "error"]),
    ...mapState("auth", ["user"]),

    filteredPayments() {
      if (!this.paymentHistory || !this.paymentHistory.data) {
        return [];
      }
      return this.paymentHistory.data.payments || [];
    },

    pagination() {
      if (!this.paymentHistory || !this.paymentHistory.data) {
        return { page: 1, limit: 10, totalPages: 1, totalResults: 0 };
      }
      return (
        this.paymentHistory.data.pagination || {
          page: 1,
          limit: 10,
          totalPages: 1,
          totalResults: 0,
        }
      );
    },
  },
  methods: {
    async retryLoading() {
      this.$store.commit("payments/SET_ERROR", null);
      await this.fetchPaymentHistory();
    },

    async fetchPaymentHistory() {
      // Build query parameters from filters
      const queryParams = {};

      if (this.filters.status) queryParams.status = this.filters.status;
      if (this.filters.type) queryParams.type = this.filters.type;
      if (this.filters.gateway) queryParams.gateway = this.filters.gateway;
      if (this.filters.startDate)
        queryParams.startDate = this.filters.startDate;
      if (this.filters.endDate) queryParams.endDate = this.filters.endDate;
      if (this.filters.sortBy) queryParams.sortBy = this.filters.sortBy;
      if (this.filters.limit) queryParams.limit = this.filters.limit;
      if (this.filters.page) queryParams.page = this.filters.page;

      await this.$store.dispatch("payments/getPaymentHistory", queryParams);
    },

    applyFilters() {
      this.fetchPaymentHistory();
    },

    resetFilters() {
      this.filters = {
        status: "",
        type: "",
        gateway: "",
        startDate: "",
        endDate: "",
        sortBy: "",
        limit: 10,
        page: 1,
      };
      this.fetchPaymentHistory();
    },

    prevPage() {
      if (this.pagination.page > 1) {
        this.filters.page = this.pagination.page - 1;
        this.fetchPaymentHistory();
      }
    },

    nextPage() {
      if (this.pagination.page < this.pagination.totalPages) {
        this.filters.page = this.pagination.page + 1;
        this.fetchPaymentHistory();
      }
    },

    formatDate(dateString, includeTime = false) {
      if (!dateString) return 'N/A';
      
      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
      };
      
      if (includeTime) {
        options.hour = "2-digit";
        options.minute = "2-digit";
      }
      
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    
    getStatusVariant(status) {
      switch (status) {
        case 'completed':
          return 'success';
        case 'failed':
          return 'destructive';
        case 'pending':
          return 'warning';
        default:
          return 'secondary';
      }
    },
    
    continuePayment(payment) {
      // Implement continue payment logic
      this.$store.dispatch('auth/showNotification', {
        type: 'info',
        message: 'Continuing payment process...',
      });
      
      // Redirect to payment gateway or relevant page
      // this.$router.push(`/payment/${payment.id}/continue`);
    },
    
    viewReceipt(payment) {
      // Implement receipt view logic
      this.$store.dispatch('auth/showNotification', {
        type: 'info',
        message: 'Generating receipt...',
      });
      
      // Open receipt in new tab or modal
      // window.open(`/api/payments/receipt/${payment.id}`, '_blank');
    },
  },
  async mounted() {
    if (!this.user) {
      this.$router.push("/auth/login");
      return;
    }
    await this.fetchPaymentHistory();
  },
};
</script>
