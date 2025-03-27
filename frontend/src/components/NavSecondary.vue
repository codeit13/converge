<template>
  <SidebarGroup>
    <SidebarGroupContent>
      <SidebarMenu>
        <SidebarMenuItem>
          <!-- <SidebarMenuButton class="text-center mx-auto" @click="handleUpgrade">
            Get Pro
          </SidebarMenuButton> -->
          <button
            class="pricing-button flex justify-between items-center gap-2 w-full"
            @click="handleUpgrade"
          >
            <!-- <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 36 24"
              class="w-4 h-4 text-white"
            >
              <path d="m18 0 8 12 10-8-4 20H4L0 4l10 8 8-12z"></path>
            </svg> -->
            Subscribe Pro
          </button>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarGroupContent>
  </SidebarGroup>
</template>

<script setup>
import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
</script>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    handleUpgrade() {
      this.$router.push("/pricing");
    },
  },
};
</script>

<style scoped>
.pricing-button {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 12px 4px;
  width: 100%;
  color: #e3e3e3;
  text-transform: uppercase;
  margin-bottom: 1.5rem;
  letter-spacing: 2px;
  font-weight: 600;
  overflow: hidden;
  border-radius: 6px;
  transition: all 0.5s ease-in-out;
}
.pricing-button {
  background: #03e9f480;
  color: #e3e3e3;
  box-shadow: 0 0 0px #03e9f4, 0 0 4000px #03e9f4;
  -webkit-box-reflect: below 2px linear-gradient(transparent, #0005);
}

.pricing-button:hover {
  background: #03e9f4;
  color: #0d0d0d;
  font-weight: 800;
  -webkit-box-reflect: none;
}
.pricing-button span {
  position: absolute;
  display: block;
}
.pricing-button span:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #03e9f4);
  animation: animate1 1s linear infinite;
}
@keyframes animate1 {
  0% {
    left: -100%;
  }
  50%,
  100% {
    left: 100%;
  }
}
.pricing-button span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #03e9f4);
  animation: animate2 1s linear infinite;
  animation-delay: 0.25s;
}
@keyframes animate2 {
  0% {
    top: -100%;
  }
  50%,
  100% {
    top: 100%;
  }
}
.pricing-button span:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #03e9f4);
  animation: animate3 1s linear infinite;
  animation-delay: 0.5s;
}
@keyframes animate3 {
  0% {
    right: -100%;
  }
  50%,
  100% {
    right: 100%;
  }
}

.pricing-button span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #03e9f4);
  animation: animate4 1s linear infinite;
  animation-delay: 0.75s;
}
@keyframes animate4 {
  0% {
    bottom: -100%;
  }
  50%,
  100% {
    bottom: 100%;
  }
}
</style>
