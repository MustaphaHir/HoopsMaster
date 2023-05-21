<template>
  <div>
    <h1>Admin Login</h1>
    <form @submit="login">
      <label>Password:</label>
      <input type="password" v-model="password" required />
      <button type="submit">Connexion</button>
      <p v-if="wrongPassword">Mauvais mot de passe</p>
    </form>
  </div>
</template>

<script>
import QuizApiService from '../services/QuizApiService';
import ParticipationStorageService from '../services/ParticipationStorageService';

export default {
  data() {
    return {
      password: '',
      wrongPassword: false,
    };
  },
  methods: {
    async login(event) {
      event.preventDefault();

      try {
        // Vérification du mot de passe
        if (this.password === 'admin123') {
          // Appeler la fonction Authentificate() de QuizApiService
          QuizApiService.authenticate('flask2023')
            .then(response => {
              // Enregistrement du token dans le localStorage
              ParticipationStorageService.saveTokenToStorage(response.data.token);

              // Redirection vers la page d'administration
              this.$router.push('/admin/questions').then(() => {
                window.location.reload();
              });


            })
            .catch(error => {
              console.error(error);
              // Afficher le message d'erreur approprié
              this.wrongPassword = true;
            });
        } else {
          // Mot de passe incorrect, afficher le message d'erreur
          this.wrongPassword = true;
        }
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
