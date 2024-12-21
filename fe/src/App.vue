<script>
import { RouterView, useRoute } from 'vue-router';
import Header from './components/Header.vue';
import Sidebar from './components/Sidebar.vue';
import { computed } from 'vue';

export default {
  components: {
    Header,
    Sidebar,
    RouterView,
  },
  setup() {
    const route = useRoute();
    const showLayout = computed(() => route.meta.layout !== 'auth'); // Pastikan selalu bereaksi terhadap perubahan rute
    return { showLayout };
  },
};
</script>

<template>
  <div id="app">
    <Sidebar v-if="showLayout" />
    <div :class="['main-content', { 'no-sidebar': !showLayout }]">
      <Header v-if="showLayout" />
      <div :class="showLayout ? 'content' : 'login-content'">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style>
#app {
  display: flex;
  background: #f5f5f5;
  height: 100vh; /* Full viewport height */
  overflow: hidden; /* Prevent body scroll */
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  margin-left: 280px;
  width: 100vw; /* Adjust to sidebar width */
  margin-top: 96px; /* Match Header height */
  overflow: hidden; /* Prevent main-content scroll */
}

.main-content.no-sidebar {
  margin: auto; /* Pusatkan elemen di dalam kontainer */
  display: flex;
  justify-content: center; /* Pusatkan secara horizontal */
  align-items: center; /* Pusatkan secara vertikal */
  height: 100%; /* Pastikan tinggi elemen sama dengan kontainer */
  width: 100%; /* Pastikan lebar elemen sama dengan kontainer */
}

.content {
  flex-grow: 1;
  overflow-y: auto; /* Only vertical scroll if needed */
  overflow-x: hidden; /* Prevent horizontal scroll */
  padding: 20px;
  background-color: #f8f9fa;
  box-sizing: border-box; /* Ensure padding doesn’t add extra width */
}
</style>
