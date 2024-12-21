<template>
  <div class="sidebar">
    <div class="sidebar-top">
      <div class="logo">
        <IoSharpLeaf class="logo-icon"/>
        <h1>Smart Waste</h1>
      </div>
      <div class="dashboard">
        <RouterLink to="/" class="button-dashboard">Dashboard <RaDashboard/></RouterLink>
      </div>
    </div>
    <div class="sidebar-middle">
      <div v-for="item in apiData" :key="item.id">
        <RouterLink :to="item.link" class="navigation">
          <component
            :is="getIconComponent(item.icon)"
            class="icon"
            v-if="getIconComponent(item.icon)"
          />
          <p>{{ item.text }}</p>
        </RouterLink>
      </div>
    </div>
    <div class="sidebar-bottom">
      <div v-for="item in apiData2" :key="item.id">
        <RouterLink :to="item.link" class="navigation">
          <component
            :is="getIconComponent(item.icon)"
            class="icon"
            v-if="getIconComponent(item.icon)"
          />
          <p>{{ item.text }}</p>
        </RouterLink>
      </div>
    </div>
  </div>
  <Header />
</template>


<script>
import { RaDashboard, AkClipboard, IcTimer, TaHelp, BySettings, IoSharpLeaf } from '@kalimahapps/vue-icons';
import Header from './Header.vue';

export default {
  components: {
    RaDashboard,
    IoSharpLeaf
  },
  data() {
    return {
      apiData: [
        { id: 1, icon: 'AkClipboard', text: 'Product', link: '/' },
        { id: 2, icon: 'IcTimer', text: 'Bid', link: '/bid' },
        // Tambahkan data lainnya sesuai response API
      ],
      apiData2: [
        { id: 1, icon: 'TaHelp', text: 'Help Center', link: '#' },
        { id: 2, icon: 'BySettings', text: 'Setting', link: '#' },
        // Tambahkan data lainnya sesuai response API
      ],
      iconMap: {
        AkClipboard,
        IcTimer,
        TaHelp,
        BySettings,
        // Tambahkan semua ikon yang diperlukan di sini
      },
    };
  },
  methods: {
    getIconComponent(iconName) {
      return this.iconMap[iconName] || null;
    },
  },
}
</script>

<style>
.logo {
  display: flex;
  align-items: center;
}

.logo h1 {
  margin: 16px;
  font-size: 22px;
}

.logo-icon {
  font-size: 24px;
  color: #27A376;
}

.sidebar {
  position: fixed; /* Make sure the sidebar stays fixed on the left */
  left: 0;
  top: 0;
  z-index: 1;
  color: #fff;
  width: 280px;
  height: 100vh;
  background-color: #1F2937;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow-y: auto; /* Allow scrolling inside sidebar if content overflows */
}

.sidebar-middle,
.sidebar-bottom {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.sidebar-middle {
  flex-grow: 1;
  margin-top: 20px;
}

.navigation {
  color: #fff;
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 10px;
}

.navigation p {
  margin: 8px;
}

.dashboard {
  display: flex;
  justify-content: center;
}

.button-dashboard {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  text-decoration: none;
  width: 100%;
  height: 56px;
  color: #fff;
  letter-spacing: 0.3px;
  font-size: 16px;
  font-weight: 700;
  background: #0CAF60;
  box-shadow: 0px 10px 30px rgba(12, 175, 96, 0.2);
  border-radius: 10px;
}
</style>