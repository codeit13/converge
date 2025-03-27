<template>
  <div
    class="fixed top-0 left-0 w-full h-full bg-black/50 z-50 flex items-center justify-center"
    v-if="isLoading"
  >
    <div class="absolute backdrop-blur-sm bg-zinc-900/50 w-full h-full"></div>
    <div class="flex items-center justify-center w-full h-full">
      <div class="bar">
        <div class="ball">
          <div class="pulse"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Loader",
  computed: {
    ...mapState(["isLoading"]),
  },
};
</script>

<style scoped>
.ball {
  position: relative;
  bottom: 50px;
  left: calc(100% - 20px);
  width: 50px;
  height: 50px;
  background: #e3e3e3 !important;
  border-radius: 50%;
  animation: ball-move 1.2s ease-in-out infinite alternate,
    glow 1.2s ease-in-out infinite alternate;
  box-shadow: 0 0 30px #fff;
  border: 2px solid rgba(255, 255, 255, 0.8);
}

.ball::after {
  position: absolute;
  content: "";
  top: 50%;
  left: 50%;
  width: 15px;
  height: 15px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 15px rgba(0, 234, 255, 0.5);
  animation: core-pulse 2s ease-in-out infinite;
  animation: shimmer 1.5s linear infinite;
}

.pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: transparent;
  border: 2px solid rgba(0, 234, 255, 0.2);
  animation: pulse 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

.bar {
  width: 200px;
  height: 4px;
  background: linear-gradient(
    90deg,
    rgba(0, 234, 255, 0.1),
    rgba(0, 234, 255, 0.4) 50%,
    rgba(0, 234, 255, 0.1)
  );
  border-radius: 4px;
  transform: rotate(-15deg);
  animation: up-down 1s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
  box-shadow: 0 0 20px rgba(0, 234, 255, 0.3);
  position: relative;
  /* overflow: hidden; */
}

/* .bar::after {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 40%;
  height: 100%;
  border-radius: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(0, 234, 255, 0.8),
    transparent
  );
  animation: shimmer 1.5s linear infinite;
} */

@keyframes up-down {
  from {
    transform: rotate(-15deg) translateY(0);
  }
  to {
    transform: rotate(15deg) translateY(-8px);
  }
}

@keyframes ball-move {
  0% {
    left: calc(100% - 40px);
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(180deg);
  }
  100% {
    left: calc(0% - 20px);
    transform: rotate(360deg);
  }
}

@keyframes glow {
  0% {
    box-shadow: 0 0 30px #ff6b6b;
    background: #ff6b6b;
  }
  33% {
    box-shadow: 0 0 35px #4ecdc4;
    background: #4ecdc4;
  }
  66% {
    box-shadow: 0 0 40px #ffe66d;
    background: #ffe66d;
  }
  100% {
    box-shadow: 0 0 30px #ff6b6b;
    background: #ff6b6b;
  }
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.8;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 0;
  }
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 200%;
  }
}
</style>
