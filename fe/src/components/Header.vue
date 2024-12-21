<template>
  <header class="header">
    <div class="right-header">
      <button class="header-button"><IcMessageText class="icon-message" /></button>
      <el-dropdown trigger="click">
        <el-button class="header-button profile-button">
          <img class="profile-image" :src="avatar" alt="Profile" />
          <AkChevronDown class="profile-dropdown" />
        </el-button>
        <template #dropdown>
          <div class="custom-dropdown-content">
            <span class="user-label">{{ username }}</span>
            <el-button
              class="button-dropwdown-logout"
              type="primary"
              @click="handleLogout"
            >
              Logout
            </el-button>
          </div>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script>
import { IcMessageText, AkChevronDown } from '@kalimahapps/vue-icons';
import ToggleButton from 'primevue/togglebutton';
import Cookies from 'js-cookie';
import avatar from '@/assets/avatar.jfif';

export default {
  components: {
    IcMessageText,
    AkChevronDown,
    ToggleButton,
  },
  data() {
    return {
      avatar,
      username: localStorage.getItem('username'),
      userId: localStorage.getItem('user_id')
    };
  },
  methods: {
    async handleLogout() {
      Cookies.remove('token');
      localStorage.removeItem('username');
      localStorage.removeItem('user_id');
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 280px;
  width: calc(100% - 280px); /* Takes the remaining space */ 
  height: 96px;
  z-index: 1;
  border-bottom: 1px solid #E9EAEC;
  background-color: #fff;

  display: flex;
  align-items: center;
}
.user-label {
  font-size: 18px;
  font-weight: 600;
  color: #08090e;
}
.custom-dropdown-content {
  padding: 12px 24px;
  width: 400px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: #fff;
  display: grid;
  gap: 20px;
  text-align: center;
}

.button-dropwdown-login {
  background-color: #1F2937;
  border-radius: 10px;
  width: 120px;
  height: 38px;
  color: #fff;
}

.button-dropwdown-login:hover {
  color: #ccc;
}

.right-header {
  margin-left: auto;
  display: flex;
  align-items: center;
  margin-right: 50px;
  gap: 10px;
}
.header-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
}
.icon-message {
  font-size: 20px
}
.profile-button {
  display: flex;
  align-items: center;
  gap: 10px;
  border: none;
  background-color: transparent;
  cursor: pointer;
}
.profile-image {
  border-radius: 100%;
  width: 32px;
  height: 32px;
  background-color: #ccc;
  object-fit: cover;
}
.profile-dropdown {
  font-size: 14px;
}
</style>