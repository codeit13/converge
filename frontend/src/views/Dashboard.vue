<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <header class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-semibold">AI Sales Dashboard</h1>
        <p class="text-muted-foreground">
          Monitor your AI-powered sales and marketing performance
        </p>
      </div>
      <Button @click="refreshData" variant="outline" class="gap-2">
        <RefreshCcw class="h-4 w-4" />
        Refresh
      </Button>
    </header>

    <!-- Key Metrics Cards -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card v-for="metric in keyMetrics" :key="metric.title">
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
            {{ Math.abs(metric.trend) }}% from last month
          </p>
        </CardContent>
      </Card>
    </div>

    <!-- Charts Section -->
    <div class="grid gap-4 md:grid-cols-2">
      <!-- Conversations Chart -->
      <Card class="col-span-1">
        <CardHeader>
          <CardTitle>AI Conversations</CardTitle>
          <CardDescription>Daily conversation metrics</CardDescription>
        </CardHeader>
        <CardContent>
          <!-- Chart placeholder - integrate with your charting library -->
          <div
            class="h-[300px] flex items-center justify-center bg-muted/5 rounded-md"
          >
            Chart: Conversations over time
          </div>
        </CardContent>
      </Card>

      <!-- Conversion Rates -->
      <Card class="col-span-1">
        <CardHeader>
          <CardTitle>Conversion Rates</CardTitle>
          <CardDescription>Sales funnel performance</CardDescription>
        </CardHeader>
        <CardContent>
          <!-- Chart placeholder - integrate with your charting library -->
          <div
            class="h-[300px] flex items-center justify-center bg-muted/5 rounded-md"
          >
            Chart: Conversion funnel
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Recent Activities Table -->
    <Card>
      <CardHeader>
        <CardTitle>Recent AI Activities</CardTitle>
        <CardDescription
          >Latest automated interactions and outcomes</CardDescription
        >
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Time</TableHead>
              <TableHead>AI Agent</TableHead>
              <TableHead>Action</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Outcome</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="activity in recentActivities" :key="activity.id">
              <TableCell>{{ activity.time }}</TableCell>
              <TableCell>{{ activity.agent }}</TableCell>
              <TableCell>{{ activity.action }}</TableCell>
              <TableCell>
                <Badge
                  :variant="
                    activity.status === 'completed' ? 'default' : 'destructive'
                  "
                >
                  {{ activity.status }}
                </Badge>
              </TableCell>
              <TableCell>{{ activity.outcome }}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  </div>
</template>

<!-- Component imports using script setup -->
<script setup>
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
  RefreshCcw,
  TrendingUp,
  TrendingDown,
  Users,
  MessageSquare,
  Target,
  DollarSign,
} from "lucide-vue-next";
</script>

<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      keyMetrics: [
        {
          title: "Total Leads",
          value: "2,834",
          trend: 12.5,
          icon: Users,
        },
        {
          title: "Conversations",
          value: "1,429",
          trend: 8.2,
          icon: MessageSquare,
        },
        {
          title: "Conversion Rate",
          value: "24.8%",
          trend: -2.1,
          icon: Target,
        },
        {
          title: "Revenue",
          value: "$48.2K",
          trend: 15.3,
          icon: DollarSign,
        },
      ],
      recentActivities: [
        {
          id: 1,
          time: "2 mins ago",
          agent: "Sales Bot",
          action: "Lead Qualification",
          status: "completed",
          outcome: "Qualified Lead",
        },
        {
          id: 2,
          time: "15 mins ago",
          agent: "Marketing Bot",
          action: "Email Campaign",
          status: "completed",
          outcome: "2.5k Emails Sent",
        },
        {
          id: 3,
          time: "1 hour ago",
          agent: "Support Bot",
          action: "Customer Query",
          status: "failed",
          outcome: "Escalated to Human",
        },
        {
          id: 4,
          time: "2 hours ago",
          agent: "Sales Bot",
          action: "Deal Negotiation",
          status: "completed",
          outcome: "Contract Sent",
        },
      ],
    };
  },
  computed: {
    ...mapState({
      // Map any required state from Vuex
    }),
  },
  methods: {
    refreshData() {
      // Implement refresh logic
      this.$store.dispatch("auth/showNotification", {
        type: "info",
        message: "Refreshing dashboard data...",
      });
    },
  },

  mounted() {
    // Load initial data
  },
};
</script>
