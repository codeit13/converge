<template>
  <div class="container mx-auto py-8 px-4">
    <!-- Main Layout with Sidebar and Content Area -->
    <div class="flex flex-col lg:flex-row gap-6">
      <!-- Sidebar Navigation -->
      <div class="w-full lg:w-64 shrink-0">
        <div class="sticky top-4">
          <Card>
            <CardHeader>
              <CardTitle>Workflows</CardTitle>
              <CardDescription>Manage your AI tasks</CardDescription>
            </CardHeader>
            <CardContent>
              <div class="space-y-2">
                <Button 
                  variant="ghost" 
                  class="w-full justify-start" 
                  :class="{ 'bg-muted': activeView === 'list' }" 
                  @click="setActiveView('list')"
                >
                  <LayoutGridIcon class="mr-2 h-4 w-4" />
                  All Workflows
                </Button>
                <Button 
                  variant="ghost" 
                  class="w-full justify-start" 
                  :class="{ 'bg-muted': activeView === 'create' }" 
                  @click="setActiveView('create')"
                >
                  <PlusIcon class="mr-2 h-4 w-4" />
                  Create New
                </Button>
                <Separator class="my-2" />
                <p class="text-sm font-medium">Recent Workflows</p>
                <div v-for="workflow in recentWorkflows" :key="workflow.id" class="py-1">
                  <Button 
                    variant="ghost" 
                    class="w-full justify-start text-sm truncate" 
                    :class="{ 'bg-muted': selectedWorkflow?.id === workflow.id && activeView === 'detail' }" 
                    @click="viewWorkflowDetail(workflow.id)"
                  >
                    {{ workflow.name }}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- Main Content Area -->
      <div class="flex-1 space-y-6">
        <!-- List View -->
        <div v-if="activeView === 'list'">
          <Card>
            <CardHeader class="flex flex-row items-center justify-between">
              <div>
                <CardTitle>All Workflows</CardTitle>
                <CardDescription>Manage and run your automated workflows</CardDescription>
              </div>
              <Button @click="setActiveView('create')">
                <PlusIcon class="mr-2 h-4 w-4" />
                New Workflow
              </Button>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Schedule</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Last Run</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow v-for="workflow in workflows" :key="workflow.id">
                    <TableCell class="font-medium">{{ workflow.name }}</TableCell>
                    <TableCell>
                      <Badge variant="outline">{{ workflow.type }}</Badge>
                    </TableCell>
                    <TableCell>{{ workflow.schedule }}</TableCell>
                    <TableCell>
                      <Badge 
                        :variant="workflow.status === 'active' ? 'default' : 'secondary'"
                      >
                        {{ workflow.status }}
                      </Badge>
                    </TableCell>
                    <TableCell>{{ formatDate(workflow.lastRun) }}</TableCell>
                    <TableCell>
                      <div class="flex space-x-2">
                        <Button 
                          variant="ghost" 
                          size="icon"
                          @click="viewWorkflowDetail(workflow.id)"
                          title="View Details"
                        >
                          <EyeIcon class="h-4 w-4" />
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="icon"
                          @click="runWorkflow(workflow.id)"
                          title="Run Workflow"
                        >
                          <PlayIcon class="h-4 w-4" />
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="icon"
                          @click="viewWorkflowDetail(workflow.id, 'history')"
                          title="View History"
                        >
                          <HistoryIcon class="h-4 w-4" />
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="icon"
                          @click="confirmDeleteWorkflow(workflow.id)"
                          title="Delete Workflow"
                        >
                          <TrashIcon class="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>

        <!-- Create View -->
        <div v-if="activeView === 'create'">
          <Card>
            <CardHeader>
              <div class="flex items-center">
                <Button 
                  variant="ghost" 
                  size="icon" 
                  class="mr-2"
                  @click="setActiveView('list')"
                >
                  <ArrowLeftIcon class="h-4 w-4" />
                </Button>
                <div>
                  <CardTitle>Create New Workflow</CardTitle>
                  <CardDescription>Set up a new automated workflow</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <form @submit.prevent="createWorkflow" class="space-y-4">
                <div class="grid gap-2">
                  <Label for="name">Name</Label>
                  <Input id="name" v-model="newWorkflow.name" placeholder="Daily News Digest" />
                </div>
                <div class="grid gap-2">
                  <Label for="description">Description</Label>
                  <Textarea 
                    id="description" 
                    v-model="newWorkflow.description"
                    placeholder="Describe what this workflow does"
                  />
                </div>
                <div class="grid gap-2">
                  <Label for="type">Type</Label>
                  <Select v-model="newWorkflow.type">
                    <option value="content">Content</option>
                    <option value="research">Research</option>
                    <option value="data">Data</option>
                    <option value="automation">Automation</option>
                  </Select>
                </div>
                <div class="grid gap-2">
                  <Label for="schedule">Schedule</Label>
                  <Select v-model="newWorkflow.schedule">
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                  </Select>
                </div>
                <div class="flex justify-end">
                  <Button type="submit">
                    <SaveIcon class="mr-2 h-4 w-4" />
                    Create Workflow
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>

        <!-- Detail View -->
        <div v-if="activeView === 'detail' && selectedWorkflow">
          <Card>
            <CardHeader>
              <div class="flex items-center">
                <Button 
                  variant="ghost" 
                  size="icon" 
                  class="mr-2"
                  @click="setActiveView('list')"
                >
                  <ArrowLeftIcon class="h-4 w-4" />
                </Button>
                <div class="flex-1">
                  <div class="flex items-center justify-between">
                    <CardTitle>{{ selectedWorkflow.name }}</CardTitle>
                    <Badge 
                      :variant="selectedWorkflow.status === 'active' ? 'default' : 'secondary'"
                    >
                      {{ selectedWorkflow.status }}
                    </Badge>
                  </div>
                  <CardDescription>{{ selectedWorkflow.description }}</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <Tabs v-model="activeTab">
                <TabsList class="grid w-full grid-cols-3">
                  <TabsTrigger value="overview">Overview</TabsTrigger>
                  <TabsTrigger value="history">History</TabsTrigger>
                  <TabsTrigger value="settings">Settings</TabsTrigger>
                </TabsList>
                
                <!-- Overview Tab -->
                <TabsContent value="overview" class="space-y-4">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card>
                      <CardHeader>
                        <CardTitle>Details</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <dl class="space-y-2">
                          <div>
                            <dt class="text-sm font-medium text-muted-foreground">Type</dt>
                            <dd>{{ selectedWorkflow.type }}</dd>
                          </div>
                          <div>
                            <dt class="text-sm font-medium text-muted-foreground">Schedule</dt>
                            <dd>{{ selectedWorkflow.schedule }}</dd>
                          </div>
                          <div>
                            <dt class="text-sm font-medium text-muted-foreground">Last Run</dt>
                            <dd>{{ formatDate(selectedWorkflow.lastRun) }}</dd>
                          </div>
                        </dl>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader>
                        <CardTitle>Actions</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div class="space-y-2">
                          <Button 
                            class="w-full justify-start" 
                            @click="runWorkflow(selectedWorkflow.id)"
                          >
                            <PlayIcon class="mr-2 h-4 w-4" />
                            Run Workflow
                          </Button>
                          <Button 
                            variant="outline" 
                            class="w-full justify-start"
                            @click="activeTab = 'history'"
                          >
                            <HistoryIcon class="mr-2 h-4 w-4" />
                            View History
                          </Button>
                          <Button 
                            variant="outline" 
                            class="w-full justify-start"
                            @click="activeTab = 'settings'"
                          >
                            <SaveIcon class="mr-2 h-4 w-4" />
                            Edit Settings
                          </Button>
                          <Button 
                            variant="destructive" 
                            class="w-full justify-start"
                            @click="confirmDeleteWorkflow(selectedWorkflow.id)"
                          >
                            <TrashIcon class="mr-2 h-4 w-4" />
                            Delete Workflow
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </TabsContent>
                
                <!-- History Tab -->
                <TabsContent value="history" class="space-y-4">
                  <Card>
                    <CardHeader>
                      <CardTitle>Execution History</CardTitle>
                      <CardDescription>Past runs of this workflow</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div v-if="isLoading" class="flex justify-center p-4">
                        <div class="animate-spin h-6 w-6 border-2 border-primary border-t-transparent rounded-full"></div>
                      </div>
                      <div v-else-if="historyItems.length === 0" class="text-center py-8">
                        <p class="text-muted-foreground">No history available</p>
                      </div>
                      <Table v-else>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Date</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Duration</TableHead>
                            <TableHead>Actions</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          <TableRow v-for="item in historyItems" :key="item.id">
                            <TableCell>{{ formatDate(item.runDate) }}</TableCell>
                            <TableCell>
                              <Badge 
                                :variant="item.status === 'completed' ? 'default' : 'destructive'"
                              >
                                {{ item.status }}
                              </Badge>
                            </TableCell>
                            <TableCell>{{ item.duration }}</TableCell>
                            <TableCell>
                              <Button 
                                variant="ghost" 
                                size="sm"
                                @click="viewOutputInDrawer(item)"
                              >
                                View Output
                              </Button>
                            </TableCell>
                          </TableRow>
                        </TableBody>
                      </Table>
                    </CardContent>
                  </Card>
                </TabsContent>
                
                <!-- Settings Tab -->
                <TabsContent value="settings" class="space-y-4">
                  <Card>
                    <CardHeader>
                      <CardTitle>Edit Workflow</CardTitle>
                      <CardDescription>Update workflow settings</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <form @submit.prevent="updateWorkflow" class="space-y-4">
                        <div class="grid gap-2">
                          <Label for="edit-name">Name</Label>
                          <Input id="edit-name" v-model="editWorkflow.name" />
                        </div>
                        <div class="grid gap-2">
                          <Label for="edit-description">Description</Label>
                          <Textarea
                            id="edit-description"
                            v-model="editWorkflow.description"
                          />
                        </div>
                        <div class="grid gap-2">
                          <Label for="edit-schedule">Schedule</Label>
                          <Select v-model="editWorkflow.schedule">
                            <option value="daily">Daily</option>
                            <option value="weekly">Weekly</option>
                            <option value="monthly">Monthly</option>
                          </Select>
                        </div>
                        <div class="grid gap-2">
                          <Label for="edit-type">Type</Label>
                          <Select v-model="editWorkflow.type">
                            <option value="content">Content</option>
                            <option value="research">Research</option>
                            <option value="data">Data</option>
                            <option value="automation">Automation</option>
                          </Select>
                        </div>
                        <div class="grid gap-2">
                          <Label for="edit-status">Status</Label>
                          <Select v-model="editWorkflow.status">
                            <option value="active">Active</option>
                            <option value="inactive">Inactive</option>
                          </Select>
                        </div>
                        <div class="flex justify-end">
                          <Button type="submit">
                            <SaveIcon class="mr-2 h-4 w-4" />
                            Save Changes
                          </Button>
                        </div>
                      </form>
                    </CardContent>
                  </Card>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>

    <!-- Output Details Drawer -->
    <Drawer v-model:open="showOutputDrawer" direction="right">
      <DrawerContent class="sm:max-w-md">
        <DrawerHeader>
          <DrawerTitle>Execution Details</DrawerTitle>
          <DrawerDescription>
            {{ selectedHistoryItem ? formatDate(selectedHistoryItem.runDate) : "" }}
          </DrawerDescription>
        </DrawerHeader>
        <div class="p-6">
          <div class="p-4 rounded-md bg-muted">
            <pre class="whitespace-pre-wrap text-sm">
            {{ selectedHistoryItem ? selectedHistoryItem.output : "" }}
            </pre>
          </div>
        </div>
        <DrawerFooter>
          <Button variant="outline" @click="showOutputDrawer = false">Close</Button>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>


    <!-- Delete Confirmation Dialog -->
    <AlertDialog v-model:open="showDeleteDialog">
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Are you sure?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently delete the
            workflow and all associated history.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <Button variant="outline" @click="showDeleteDialog = false">Cancel</Button>
          <Button variant="destructive" @click="deleteWorkflow">Delete</Button>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  </div>
</template>


<!-- Component imports using script setup -->
<script setup>
// Component imports only
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
} from "@/components/ui/table";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerTitle,
  DrawerDescription,
  DrawerFooter,
} from "@/components/ui/drawer";
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogFooter,
} from "@/components/ui/alert-dialog";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
</script>

<script>
// 1. Third-party imports
import { mapState } from "vuex";
import {
  PlusIcon,
  ClockIcon,
  CalendarIcon,
  PlayIcon,
  HistoryIcon,
  RocketIcon,
  LayoutGridIcon,
  ArrowLeftIcon,
  EyeIcon,
  TrashIcon,
  SaveIcon,
} from "lucide-vue-next";

// 2. Utility/Constants imports
import { BACKEND_URL } from "@/utils/constants";

export default {
  // 3. Props definition
  props: {},

  // 4. Component data
  data() {
    return {
      workflows: [
        {
          id: 1,
          name: "Daily Tech News",
          description:
            "Scrapes Twitter, Google for trending tech news and creates a Medium article",
          status: "active",
          schedule: "Daily at 8:00 AM",
          lastRun: new Date(Date.now() - 86400000), // yesterday
          type: "content",
        },
        {
          id: 2,
          name: "Weekly AI Research Digest",
          description:
            "Compiles latest AI research papers and summarizes findings",
          status: "inactive",
          schedule: "Weekly on Monday",
          lastRun: new Date(Date.now() - 604800000), // last week
          type: "research",
        },
      ],
      // UI state management
      activeView: 'list', // 'list', 'create', 'detail'
      activeTab: 'overview', // 'overview', 'history', 'settings'
      
      // Modal state (legacy - will be removed)
      showHistoryDialog: false,
      showOutputDialog: false,
      showNewWorkflowDialog: false,
      
      // New UI state
      showOutputDrawer: false,
      showDeleteDialog: false,
      
      // Data state
      selectedWorkflow: null,
      selectedHistoryItem: null,
      historyItems: [],
      newWorkflow: {
        name: "",
        description: "",
        schedule: "daily",
        type: "content",
      },
      editWorkflow: {
        id: null,
        name: "",
        description: "",
        schedule: "daily",
        type: "content",
        status: "active"
      },
      isLoading: false,
    };
  },

  // 5. Computed properties
  computed: {
    ...mapState({
      jwtToken: (state) => state.JWT_TOKEN,
    }),
    
    // Get 3 most recently run workflows for the sidebar
    recentWorkflows() {
      return [...this.workflows]
        .sort((a, b) => new Date(b.lastRun) - new Date(a.lastRun))
        .slice(0, 3);
    },
  },

  // 6. Watchers
  watch: {},

  // 7. Lifecycle hooks
  created() {
    // Fetch workflows on component creation
    this.fetchWorkflows();
  },

  mounted() {},

  unmounted() {
    // Clear any intervals or subscriptions
  },

  // 8. Methods
  methods: {
    async fetchWorkflows() {
      // In a real app, this would fetch from the backend
      // this.workflows = await this.$store.dispatch('getWorkflows');
      this.isLoading = true;
      try {
        // Simulate API call
        setTimeout(() => {
          this.isLoading = false;
        }, 500);
      } catch (error) {
        console.error("Error fetching workflows:", error);
        this.isLoading = false;
      }
    },

    // Navigation methods for multi-panel layout
    setActiveView(view) {
      this.activeView = view;
      
      // Reset form when switching to create view
      if (view === 'create') {
        this.newWorkflow = {
          name: "",
          description: "",
          schedule: "daily",
          type: "content",
        };
      }
      
      // Reset detail view when going back to list
      if (view === 'list') {
        this.selectedWorkflow = null;
        this.activeTab = 'overview';
      }
    },
    
    viewWorkflowDetail(workflowId, tab = 'overview') {
      const workflow = this.workflows.find((w) => w.id === workflowId);
      if (!workflow) return;
      
      this.selectedWorkflow = workflow;
      this.activeTab = tab;
      this.activeView = 'detail';
      
      // Initialize edit form with current workflow data
      this.editWorkflow = { ...workflow };
      
      // If history tab is selected, fetch history
      if (tab === 'history') {
        this.fetchWorkflowHistory(workflowId);
      }
    },
    
    async runWorkflow(workflowId) {
      try {
        const workflow = this.workflows.find((w) => w.id === workflowId);
        if (!workflow) return;

        // Prompt the user for natural language task description
        const taskDescription = prompt("What task would you like to execute?", "");
        
        // If user cancels the prompt or provides empty input
        if (!taskDescription) {
          this.$toast.info("Workflow execution cancelled");
          return;
        }

        const agentData = {
          workflowId: workflowId,
          type: workflow.type,
          messages: taskDescription // Pass the natural language string
        };

        const result = await this.$store.dispatch("runAgent", agentData);

        // Show success notification
        this.$toast.success(`Workflow "${workflow.name}" started successfully`);

        // Update the workflow's last run time
        workflow.lastRun = new Date();
        
        // If we're in detail view, refresh history
        if (this.activeView === 'detail' && this.activeTab === 'history' && this.selectedWorkflow?.id === workflowId) {
          this.fetchWorkflowHistory(workflowId);
        }

        return result;
      } catch (error) {
        console.error("Error running workflow:", error);
        this.$toast.error("Failed to run workflow. Please try again.");
      }
    },

    // Legacy method - will be replaced by fetchWorkflowHistory
    async viewHistory(workflowId) {
      this.selectedWorkflow = this.workflows.find((w) => w.id === workflowId);
      if (!this.selectedWorkflow) return;

      this.isLoading = true;
      try {
        const history = await this.$store.dispatch("getHistory", workflowId);
        this.historyItems = history;
        this.isLoading = false;
        this.showHistoryDialog = true;
      } catch (error) {
        console.error("Error fetching workflow history:", error);
        this.isLoading = false;
      }
    },
    
    // New method for fetching workflow history in the redesigned UI
    async fetchWorkflowHistory(workflowId) {
      if (!workflowId) return;
      
      this.isLoading = true;
      try {
        const history = await this.$store.dispatch("getHistory", workflowId);
        this.historyItems = history;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching workflow history:", error);
        this.$toast.error("Failed to fetch workflow history");
        this.isLoading = false;
      }
    },

    // Legacy method - will be replaced by viewOutputInDrawer
    viewOutput(historyItem) {
      this.selectedHistoryItem = historyItem;
      this.showOutputDialog = true;
    },
    
    // New method for viewing output in a drawer instead of a modal
    viewOutputInDrawer(historyItem) {
      this.selectedHistoryItem = historyItem;
      this.showOutputDrawer = true;
    },

    // Legacy method - will be replaced by setActiveView('create')
    openNewWorkflowDialog() {
      this.newWorkflow = {
        name: "",
        description: "",
        schedule: "daily",
        type: "content",
      };
      this.showNewWorkflowDialog = true;
    },

    // Create workflow in the new UI
    async createWorkflow() {
      if (!this.newWorkflow.name || !this.newWorkflow.description) {
        this.$toast.error("Please fill in all required fields");
        return;
      }

      try {
        // In a real app, this would send to the backend
        // const result = await this.$store.dispatch('createWorkflow', this.newWorkflow);

        // Simulate API call
        const newId = this.workflows.length + 1;
        const newWorkflow = {
          id: newId,
          name: this.newWorkflow.name,
          description: this.newWorkflow.description,
          status: "inactive",
          schedule: this.formatSchedule(this.newWorkflow.schedule),
          lastRun: null,
          type: this.newWorkflow.type,
        };

        this.workflows.push(newWorkflow);
        
        // In the new UI, we navigate back to the list view after creating
        if (this.activeView === 'create') {
          this.setActiveView('list');
        } else {
          // Legacy support
          this.showNewWorkflowDialog = false;
        }
        
        this.$toast.success("Workflow created successfully");
      } catch (error) {
        console.error("Error creating workflow:", error);
        this.$toast.error("Failed to create workflow. Please try again.");
      }
    },
    
    // Update an existing workflow
    async updateWorkflow() {
      if (!this.editWorkflow.id || !this.editWorkflow.name || !this.editWorkflow.description) {
        this.$toast.error("Please fill in all required fields");
        return;
      }
      
      try {
        // In a real app, this would send to the backend
        // const result = await this.$store.dispatch('updateWorkflow', this.editWorkflow);
        
        // Simulate API call
        const index = this.workflows.findIndex(w => w.id === this.editWorkflow.id);
        if (index !== -1) {
          // Update the workflow with edited values
          this.workflows[index] = {
            ...this.editWorkflow,
            schedule: this.formatSchedule(this.editWorkflow.schedule)
          };
          
          // Also update the selected workflow if we're in detail view
          if (this.selectedWorkflow?.id === this.editWorkflow.id) {
            this.selectedWorkflow = this.workflows[index];
          }
          
          this.$toast.success("Workflow updated successfully");
        }
      } catch (error) {
        console.error("Error updating workflow:", error);
        this.$toast.error("Failed to update workflow. Please try again.");
      }
    },
    
    // Show delete confirmation dialog
    confirmDeleteWorkflow(workflowId) {
      this.selectedWorkflow = this.workflows.find(w => w.id === workflowId);
      if (!this.selectedWorkflow) return;
      
      this.showDeleteDialog = true;
    },
    
    // Delete a workflow
    async deleteWorkflow() {
      if (!this.selectedWorkflow) {
        this.showDeleteDialog = false;
        return;
      }
      
      try {
        // In a real app, this would send to the backend
        // await this.$store.dispatch('deleteWorkflow', this.selectedWorkflow.id);
        
        // Simulate API call
        const index = this.workflows.findIndex(w => w.id === this.selectedWorkflow.id);
        if (index !== -1) {
          this.workflows.splice(index, 1);
          this.$toast.success("Workflow deleted successfully");
          
          // If we're in detail view of the deleted workflow, go back to list
          if (this.activeView === 'detail' && this.selectedWorkflow.id === this.selectedWorkflow.id) {
            this.setActiveView('list');
          }
        }
        
        this.showDeleteDialog = false;
      } catch (error) {
        console.error("Error deleting workflow:", error);
        this.$toast.error("Failed to delete workflow. Please try again.");
        this.showDeleteDialog = false;
      }
    },

    formatDate(date) {
      if (!date) return "Never";
      return new Date(date).toLocaleString();
    },

    formatSchedule(schedule) {
      const scheduleMap = {
        daily: "Daily at 8:00 AM",
        weekly: "Weekly on Monday",
        monthly: "Monthly on the 1st",
        custom: "Custom Schedule",
      };
      return scheduleMap[schedule] || schedule;
    },

    getStatusClass(status) {
      const statusClasses = {
        active: "bg-green-100 text-green-800",
        inactive: "bg-gray-100 text-gray-800",
        completed: "bg-green-100 text-green-800",
        failed: "bg-red-100 text-red-800",
        running: "bg-blue-100 text-blue-800",
      };
      return statusClasses[status] || "bg-gray-100 text-gray-800";
    },
  },
};
</script>

<style scoped>
/* Scoped styles */
.container {
  max-width: 1200px;
}
</style>
