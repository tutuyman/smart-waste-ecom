<template>
  <form class="card-login" @submit.prevent="handleLogin">
    <h2>Login</h2>
    <div class="login__form">
      <div class="login__form_label"><span>Email :</span></div>
      <div class="login__form_input">
        <el-input
          v-model="email"
          type="email"
          placeholder="Masukkan email"
          style="min-width: 230px"
        />
      </div>
    </div>
    <div class="login__form">
      <div class="login__form_label"><span>Password :</span></div>
      <div class="login__form_input">
        <el-input
          type="password"
          show-password
          v-model="password"
          placeholder="Masukkan password"
          style="min-width: 230px"
        />
      </div>
    </div>
    <el-button
      class="button-dropwdown-login"
      type="primary"
      @click="handleLogin"
    >
      Login
    </el-button>
  </form>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';

export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async handleLogin() {
      try {
        const base = import.meta.env.VITE_BE_BASE_URI;
        // Kirim request POST ke backend FastAPI
        const response = await axios.post(
          `${base}/api/token`,
          {
            username: this.email,
            password: this.password,
          },
        );

        // Simpan token ke cookies
        Cookies.set('token', response.data.access_token, {
          expires: 7, // Cookie berlaku selama 7 hari
          secure: false, // Aktifkan jika aplikasi Anda menggunakan HTTPS
          sameSite: 'Strict', // Mencegah pengiriman cookie ke domain lain
        });

        if (response.data.username && response.data.user_id && response.data.role) {
          localStorage.setItem('username', response.data.username);
          localStorage.setItem('user_id', response.data.user_id);
          localStorage.setItem('role', response.data.role);
        } else {
          console.error('Data yang diterima tidak lengkap:', response.data);
        }

        this.$router.push('/product');
      } catch (error) {
        // Tangani error login
        this.message =
          error.response && error.response.data.detail
            ? "Login gagal: " + error.response.data.detail
            : "Terjadi kesalahan saat login.";
      }
    },
  },
};
</script>

<style scoped>
.login__form {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 16px;
  font-size: 14px;
  padding-bottom: 8px;
}

.card-login {
  width: 400px; /* Lebar tetap untuk card */
  padding: 20px; /* Padding internal */
  margin: auto; /* Pusatkan elemen di kontainer */
  border-radius: 8px; /* Sudut membulat */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Bayangan untuk efek elevasi */
  background-color: #ffffff; /* Warna latar card */
  text-align: center; /* Pusatkan teks di dalam card */
  display: flex;
  flex-direction: column;
  gap: 16px; /* Jarak antar elemen di dalam card */
}


.login__form_label {
  width: 80px;
  display: flex;
  justify-content: start;
}

</style>
