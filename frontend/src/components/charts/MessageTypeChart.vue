<template>
  <Pie :data="chartData" :options="chartOptions" />
</template>

<!-- Component imports using script setup -->
<script setup>
// Component imports only
</script>

<script>
// 1. Third-party imports
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend);

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
              },
              padding: 20
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: 'rgba(255, 255, 255, 0.9)',
            bodyColor: 'rgba(255, 255, 255, 0.9)',
            displayColors: true,
            padding: 10,
            cornerRadius: 6,
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = context.raw || 0;
                const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                const percentage = Math.round((value / total) * 100);
                return `${label}: ${value} (${percentage}%)`;
              }
            }
          }
        },
        cutout: '30%',
        animation: {
          animateScale: true,
          animateRotate: true
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
