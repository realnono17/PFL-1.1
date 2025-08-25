<template>
  <Navbar />
  <main class="content">
    <router-view />
  </main>
  <Footer />
</template>

<script>
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";

export default {
  components: {
    Navbar,
    Footer,
  },
};
</script>

<style>
.content {
  padding-top: 80px; /* Prevents content from overlapping the fixed navbar */
  padding-bottom: 80px; /* Prevents content from overlapping the fixed footer */
}
</style>
