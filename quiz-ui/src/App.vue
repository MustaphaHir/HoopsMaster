<template>
  <div id="app" class="app-container">
    <header class="sticky-header">
      <img alt="Vue logo" class="logo" src="@/assets/logo_hoops.png" />
      <div class="wrapper">

        <nav>
          <img class="menu-icon" src="@/assets/basketball-ball.png" alt="Basketball Icon" />
          <RouterLink to="/" class="nav-link">Accueil</RouterLink>

          <img class="menu-icon" src="@/assets/basketball-ball.png" alt="Basketball Icon" />
          <RouterLink to="/admin/login" class="nav-link">Admin</RouterLink>
          <img class="menu-icon" src="@/assets/basketball-ball.png" alt="Basketball Icon" />
          <button v-if="isLoggedIn" @click="logout" class="logout-button"><span>Déconnexion</span></button>


        </nav>
      </div>




    </header>

    <RouterView />
  </div>
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
.menu-icon {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

nav a.router-link-exact-active {
  color: var(--color-primary);
  background-color: transparent;
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
  position: relative;
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
  text-decoration: none;
  font-weight: bold;
  margin-right: 1rem;
  transition: color 0.3s ease, background-color 0.3s ease;
}

nav a:first-of-type {
  border: 0;
  margin-left: 0;
}

nav a::before {
  content: "";
  position: absolute;
  width: 100%;
  height: 2px;
  background-color: var(--color-text-inverse);
  bottom: -2px;
  left: 0;
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform 0.3s ease;
}

nav a:hover {
  color: var(--color-primary);
  background-color: rgba(0, 0, 0, 0.1);
}

nav a:hover::before {
  transform: scaleX(1);
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: center;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    font-size: 2rem;
    padding: 1rem 0;
    margin-top: 1rem;
    margin-left: auto;

  }


  .logout-button {
    margin-left: 1rem;
    margin-right: 10px;
    align-self: center;
  }

  .sticky-header {

    top: 0;

    z-index: 999;
    /* Autres styles de mise en forme du header */
  }
}


.logout-button {
  background-color: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.logout-button span {
  display: inline-block;
  padding: 0.5em 1em;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #ff5f58;
  border-radius: 0.5em;
  transition: transform 0.3s ease;
}

.logout-button:hover span {
  transform: translateY(-2px);
}

.logout-button::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  opacity: 0;
  transition: opacity 0.3s ease;
}

.logout-button:hover::before {
  opacity: 1;
}

.logout-button::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 200%;
  height: 200%;
  transform: translate(-50%, -50%);

  opacity: 0;
  transition: opacity 0.3s ease;
}

.logout-button:hover::after {
  opacity: 1;
}
</style>
