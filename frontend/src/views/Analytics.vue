<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <header class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-semibold">AI Conversation Dashboard</h1>
        <p class="text-muted-foreground">
          Monitor your AI-powered conversation performance
        </p>
      </div>
      <Button @click="refreshData" variant="outline" class="gap-2" :disabled="isLoading">
        <RefreshCcw v-if="!isLoading" class="h-4 w-4" />
        <Loader2 v-else class="h-4 w-4 animate-spin" />
        {{ isLoading ? 'Loading...' : 'Refresh' }}
      </Button>
    </header>

    <!-- Key Metrics Cards -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card v-for="metric in computedMetrics" :key="metric.title">
        <CardHeader>
          <CardTitle class="flex items-center gap-2 text-sm font-medium">
            <component :is="metric.icon" class="h-4 w-4" />
            {{ metric.title }}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ metric.value }}</div>
          <p
            :class="[
              'text-xs mt-1',
              metric.trend > 0 ? 'text-green-500' : 'text-red-500',
            ]"
          >
            <component
              :is="metric.trend > 0 ? TrendingUp : TrendingDown"
              class="h-3 w-3 inline"
            />
            {{ metric.trend ? Math.abs(metric.trend) + '% from last period' : 'No change' }}
          </p>
        </CardContent>
      </Card>
    </div>

    <!-- Charts Section -->
    <div class="grid gap-4 md:grid-cols-2">
      <!-- Conversations Chart -->
      <Card class="col-span-1">
        <CardHeader>
          <CardTitle>Conversation Trend</CardTitle>
          <CardDescription>Daily conversation metrics</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="h-[300px]" v-if="!isLoading && chatTrendData">
            <ConversationChart :chart-data="chatTrendData" />
          </div>
          <div
            v-else
            class="h-[300px] flex items-center justify-center bg-muted/5 rounded-md"
          >
            <Loader2 v-if="isLoading" class="h-6 w-6 animate-spin text-primary" />
            <span v-else>No data available</span>
          </div>
        </CardContent>
      </Card>

      <!-- Message Distribution -->
      <Card class="col-span-1">
        <CardHeader>
          <CardTitle>Message Types</CardTitle>
          <CardDescription>Distribution of messages by type</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="h-[300px]" v-if="!isLoading && messageTypeData">
            <MessageTypeChart :chart-data="messageTypeData" />
          </div>
          <div
            v-else
            class="h-[300px] flex items-center justify-center bg-muted/5 rounded-md"
          >
            <Loader2 v-if="isLoading" class="h-6 w-6 animate-spin text-primary" />
            <span v-else>No data available</span>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Recent Activities Table -->
    <Card>
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <div>
          <CardTitle>Recent Activities</CardTitle>
          <CardDescription>Latest conversation interactions</CardDescription>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" class="h-8 w-8 p-0">
              <span class="sr-only">Open menu</span>
              <MoreHorizontal class="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DropdownMenuItem @click="refreshData">Refresh</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem>View all</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </CardHeader>
      <CardContent>
        <div v-if="isLoading" class="flex justify-center py-4">
          <Loader2 class="h-6 w-6 animate-spin text-primary" />
        </div>
        <div v-else-if="!recentActivities || recentActivities.length === 0" class="text-center py-4 text-muted-foreground">
          No recent activities found
        </div>
        <Table v-else>
          <TableHeader>
            <TableRow>
              <TableHead>Time</TableHead>
              <TableHead>Title</TableHead>
              <TableHead>Messages</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="activity in recentActivities" :key="activity.id">
              <TableCell>{{ formatTimeAgo(activity.time) }}</TableCell>
              <TableCell>{{ activity.title }}</TableCell>
              <TableCell>{{ activity.message_count }}</TableCell>
              <TableCell>
                <Badge
                  :variant="activity.status === 'completed' ? 'default' : 'outline'"
                >
                  {{ activity.status }}
                </Badge>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  </div>
</template>

<!-- Component imports using script setup -->
<script setup>
// Component imports only
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import ConversationChart from "../components/charts/ConversationChart.vue";
import MessageTypeChart from "../components/charts/MessageTypeChart.vue";
</script>

<script>
// 1. Third-party imports
import { mapState } from "vuex";
import {
  RefreshCcw,
  TrendingUp,
  TrendingDown,
  Users,
  MessageSquare,
  Target,
  DollarSign,
  Loader2,
  MoreHorizontal,
} from "lucide-vue-next";

// 2. Utility/Constants imports
import { format, formatDistance } from 'date-fns';

export default {
  // 3. Props definition (none for this component)
  
  // 4. Component data
  data() {
    return {
      isLoading: false,
      baseMetrics: [
        {
          title: "Total Chats",
          key: "total_chats",
          trend: 0,
          icon: MessageSquare,
        },
        {
          title: "Total Messages",
          key: "total_messages",
          trend: 0,
          icon: Users,
        },
        {
          title: "Avg. Messages",
          key: "avg_messages_per_chat",
          trend: 0,
          icon: Target,
        },
        {
          title: "Completion Rate",
          key: "completion_rate",
          suffix: "%",
          trend: 0,
          icon: DollarSign,
        },
      ],
      recentActivities: [],
      chatTrendData: null,
      messageTypeData: null,
    };
  },

  // 5. Computed properties
  computed: {
    ...mapState(["availableTools", "chatSessions", "analyticsSummary", "chatDistribution"]),
    
    computedMetrics() {
      if (!this.analyticsSummary) return this.baseMetrics.map(metric => {
        return {
          ...metric,
          value: "--"
        };
      });
      
      return this.baseMetrics.map(metric => {
        let value = this.analyticsSummary[metric.key];
        
        // Format numbers over 1000 with k suffix
        if (typeof value === 'number' && value > 1000) {
          value = (value / 1000).toFixed(1) + 'k';
        }
        
        // Add suffix if specified
        if (metric.suffix) {
          value = value + metric.suffix;
        }
        
        return {
          ...metric,
          value: value.toString(),
        };
      });
    }
  },

  // 6. Watchers
  watch: {
    analyticsSummary: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.processAnalyticsData(newVal);
        }
      }
    }
  },

  // 7. Lifecycle hooks
  created() {
    // Component creation logic
  },
  
  async mounted() {
    // Load initial data
    this.refreshData();
  },

  unmounted() {
    // Cleanup any subscriptions or intervals
  },

  // 8. Methods
  methods: {
    async refreshData() {
      this.isLoading = true;
      try {
        await this.$store.dispatch("getAnalyticsSummary");
        await this.$store.dispatch("getChatDistribution");
        this.$store.dispatch("auth/showNotification", {
          type: "success",
          message: "Dashboard data refreshed",
        });
      } catch (error) {
        console.error("Error refreshing analytics data:", error);
        this.$store.dispatch("auth/showNotification", {
          type: "error",
          message: "Failed to refresh dashboard data",
        });
      } finally {
        this.isLoading = false;
      }
    },
    
    processAnalyticsData(data) {
      // Process recent activities
      if (data.recent_activity) {
        this.recentActivities = data.recent_activity.map(activity => ({
          id: activity.id,
          time: new Date(activity.time),
          title: activity.title || 'Untitled Chat',
          message_count: activity.message_count || 0,
          status: activity.status || 'started',
        }));
      }
      
      // Process chart data for conversations trend
      if (data.chat_trend && data.chat_trend.length > 0) {
        const labels = data.chat_trend.map(item => format(new Date(item.date), 'MMM d'));
        const counts = data.chat_trend.map(item => item.count);
        
        this.chatTrendData = {
          labels,
          datasets: [
            {
              label: 'Conversations',
              data: counts,
              borderColor: '#8b5cf6',
              backgroundColor: 'rgba(139, 92, 246, 0.1)',
              fill: true,
              tension: 0.4,
            },
          ],
        };
      }
      
      // Process message types for pie chart
      if (data.message_types) {
        const labels = Object.keys(data.message_types).map(key => 
          key === 'user' ? 'User Messages' : 'AI Responses'
        );
        const values = Object.values(data.message_types);
        
        this.messageTypeData = {
          labels,
          datasets: [
            {
              data: values,
              backgroundColor: ['#8b5cf6', '#ec4899'],
              borderWidth: 1,
            },
          ],
        };
      }
    },
    
    formatTimeAgo(date) {
      if (!date) return 'Unknown';
      return formatDistance(new Date(date), new Date(), { addSuffix: true });
    },
  }
};
</script>
