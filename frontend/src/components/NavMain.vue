<template>
  <SidebarGroup>
    <SidebarGroupLabel>Platform</SidebarGroupLabel>
    <SidebarGroupContent>
      <SidebarMenu>
        <template v-for="item in items" :key="item.title">
          <SidebarMenuItem v-if="!item.items">
            <SidebarMenuButton
              as-child
              class="cursor-pointer"
              :class="{
                'text-secondary bg-secondary/10 hover:bg-secondary/20':
                  isRouteActive(item.url),
              }"
              @click="navigateToRoute(item.url)"
            >
              <div class="flex w-full">
                <component :is="item.icon" class="mr-2 h-4 w-4" />
                <span>{{ item.title }}</span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <Collapsible
            v-else
            as-child
            v-model:open="openItems[item.title]"
            @update:open="(isOpen) => handleCollapsible(item.title, isOpen)"
          >
            <SidebarMenuItem class="flex w-full flex-col">
              <CollapsibleTrigger as-child>
                <SidebarMenuButton
                  class="w-full justify-between"
                  :class="{
                    'text-secondary bg-secondary/10 hover:bg-secondary/20 hover:text-secondary':
                      isRouteActive(item.url) || isItemOrChildActive(item),
                  }"
                  @click="handleMainClick(item)"
                >
                  <div class="flex items-center">
                    <component :is="item.icon" class="mr-2 h-4 w-4" />
                    <span>{{ item.title }}</span>
                  </div>
                  <ChevronRight
                    class="ml-auto h-4 w-4 transition-transform duration-200"
                    :class="{ 'rotate-90': openItems[item.title] }"
                  />
                </SidebarMenuButton>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <SidebarMenuSub>
                  <SidebarMenuSubItem
                    v-for="subItem in item.items"
                    :key="subItem.title"
                  >
                    <SidebarMenuSubButton
                      as-child
                      :class="{
                        'text-secondary font-medium': isRouteActive(
                          subItem.url
                        ),
                      }"
                      @click="navigateToRoute(subItem.url)"
                    >
                      <div class="w-full cursor-pointer">
                        {{ subItem.title }}
                      </div>
                    </SidebarMenuSubButton>
                  </SidebarMenuSubItem>
                </SidebarMenuSub>
              </CollapsibleContent>
            </SidebarMenuItem>
          </Collapsible>
        </template>
      </SidebarMenu>
    </SidebarGroupContent>
  </SidebarGroup>
</template>

<!-- Component imports using script setup -->
<script setup>
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar";
import { ChevronRight } from "lucide-vue-next";
</script>

<script>
export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
  },

  data() {
    return {
      openItems: {},
    };
  },

  computed: {
    currentRoute() {
      return this.$route.path;
    },
  },

  watch: {
    currentRoute: {
      immediate: true,
      handler() {
        this.initializeOpenItems();
      },
    },
  },

  methods: {
    initializeOpenItems() {
      this.items.forEach((item) => {
        if (item.items) {
          const isChildActive = item.items.some((child) =>
            this.isRouteActive(child.url)
          );
          if (isChildActive) {
            this.openItems[item.title] = true;
          }
        }
      });
    },

    handleCollapsible(title, isOpen) {
      if (isOpen) {
        // Close other items when opening a new one
        Object.keys(this.openItems).forEach((key) => {
          if (key !== title) {
            this.openItems[key] = false;
          }
        });
      }
      // Set the current item's state
      this.openItems[title] = isOpen;
    },

    isRouteActive(url) {
      return this.$route.path === url.split("?")[0].split("#")[0];
    },

    isItemOrChildActive(item) {
      return item.items?.some((child) => this.isRouteActive(child.url));
    },

    navigateToRoute(url) {
      if (window.innerWidth < 768) {
        this.$store.commit("SET_SIDEBAR_OPEN", false);
      }
      this.$router.push(url);
    },

    handleMainClick(item) {
      // Navigate to the main heading's URL
      this.navigateToRoute(item.url);
      // Toggle the collapsible section
      this.openItems[item.title] = !this.openItems[item.title];
    },
  },
};
</script>
