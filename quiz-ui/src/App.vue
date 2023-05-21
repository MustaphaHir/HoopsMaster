<template>
  <header>
    <div class="header-container">
      <div class="navbar">
        <nav>
          <RouterLink to="/" class="nav-link">Home</RouterLink>
          <RouterLink to="/admin/login" class="nav-link">Admin</RouterLink>
          <button v-if="isLoggedIn" @click="logout" class="logout-button">Déconnexion</button>
        </nav>
      </div>

      <img alt="Vue logo" class="logo" src="@/assets/logo_hoops_master.png" width="125" height="125" />
    </div>
  </header>

  <RouterView />
</template>

<script>
import ParticipationStorageService from './services/ParticipationStorageService';
import { RouterLink, RouterView } from 'vue-router';

export default {
  computed: {
    isLoggedIn() {
      return ParticipationStorageService.getToken() !== null;
    }
  },
  methods: {
    logout() {
      ParticipationStorageService.removeTokenFromStorage();

      this.$router.push('/').then(() => {
        window.location.reload();
      });
    }
  },
  components: {
    RouterLink,
    RouterView
  }
};
</script>

<style scoped>
header {
  background-color: #f9f9f9;
  padding: 1rem;
  line-height: 1.5;
}

.header-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.navbar {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.nav-link {
  display: inline-block;
  padding: 0.5rem 1rem;
  margin: 0 0.5rem;
  border-radius: 5px;
  text-decoration: none;
  color: #333;
  font-weight: bold;
  background-color: #fff;
  transition: background-color 0.3s ease;
}

.nav-link.router-link-exact-active {
  background-color: #333;
  color: #fff;
}

.nav-link:hover {
  background-color: #eee;
}

.logout-button {
  background-color: #e74c3c;
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #c0392b;
}

.logo {
  display: block;
}
</style>
