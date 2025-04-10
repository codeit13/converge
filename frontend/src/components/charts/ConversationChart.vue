<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<!-- Component imports using script setup -->
<script setup>
// Component imports only
</script>

<script>
// 1. Third-party imports
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js';

// Register ChartJS components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

export default {
  // 3. Props definition
  props: {
    chartData: {
      type: Object,
      required: true
    }
  },

  // 4. Component data
  data() {
    return {
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              color: 'rgba(255, 255, 255, 0.7)', // Label color for dark theme
              font: {
                family: "'Inter', sans-serif",
                size: 12,
              }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: 'rgba(255, 255, 255, 0.9)',
            bodyColor: 'rgba(255, 255, 255, 0.9)',
            displayColors: false,
            padding: 10,
            cornerRadius: 6
          }
        },
        scales: {
          x: {
            grid: {
              color: 'rgba(255, 255, 255, 0.1)', // Grid line color for dark theme
              drawBorder: false,
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.7)', // Axis label color for dark theme
              font: {
                family: "'Inter', sans-serif",
                size: 11,
              }
            }
          },
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(255, 255, 255, 0.1)', // Grid line color for dark theme
              drawBorder: false,
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.7)', // Axis label color for dark theme
              precision: 0,
              font: {
                family: "'Inter', sans-serif",
                size: 11,
              }
            }
          }
        },
        animation: {
          duration: 1000
        }
      }
    };
  },

  // 5. Computed properties (none for this component)

  // 6. Watchers (none for this component)

  // 7. Lifecycle hooks (none for this component)

  // 8. Methods (none for this component)
};
</script>

<style scoped>
/* Scoped styles */
</style>
