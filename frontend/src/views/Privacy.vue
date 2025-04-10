<template>
  <div class="privacy-container">
    <h1>Privacy Policy</h1>
    <div class="content">
      <p>Last updated: April 10, 2025</p>
      
      <section>
        <h2>1. Introduction</h2>
        <p>Welcome to Converge. This Privacy Policy explains how we collect, use, and protect your personal information.</p>
      </section>

      <section>
        <h2>2. Information We Collect</h2>
        <p>We collect information that you provide directly to us when using our services.</p>
      </section>

      <section>
        <h2>3. How We Use Your Information</h2>
        <p>We use the collected information to provide, maintain, and improve our services.</p>
      </section>

      <section>
        <h2>4. Contact Us</h2>
        <p>If you have any questions about this Privacy Policy, please contact us.</p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Privacy',
  
  data() {
    return {
      // Component data if needed
    }
  },

  mounted() {
    // Set page title
    document.title = 'Privacy Policy - Converge'
  }
}
</script>

<style scoped>
.privacy-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.content {
  margin-top: 2rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

h2 {
  font-size: 1.8rem;
  margin: 2rem 0 1rem;
}

section {
  margin-bottom: 2rem;
}

p {
  line-height: 1.6;
  margin-bottom: 1rem;
}
</style>
