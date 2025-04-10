<template>
  <div class="terms-container">
    <h1>Terms and Conditions</h1>
    <div class="content">
      <p>Last updated: April 10, 2025</p>
      
      <section>
        <h2>1. Agreement to Terms</h2>
        <p>By accessing and using Converge, you agree to be bound by these Terms and Conditions.</p>
      </section>

      <section>
        <h2>2. Use License</h2>
        <p>Permission is granted to temporarily use Converge for personal, non-commercial transitory viewing only.</p>
      </section>

      <section>
        <h2>3. Disclaimer</h2>
        <p>The materials on Converge are provided on an 'as is' basis.</p>
      </section>

      <section>
        <h2>4. Limitations</h2>
        <p>In no event shall Converge or its suppliers be liable for any damages arising out of the use or inability to use the materials on Converge.</p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TermsAndConditions',
  
  data() {
    return {
      // Component data if needed
    }
  },

  mounted() {
    // Set page title
    document.title = 'Terms and Conditions - Converge'
  }
}
</script>

<style scoped>
.terms-container {
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
