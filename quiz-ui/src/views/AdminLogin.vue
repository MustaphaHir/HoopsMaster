<template>
  <div class="admin-login-page">
    <h1>Page de connexion ADMIN</h1>
    <form @submit="login" class="login-form">
      <div class="form-group">
        <label for="password">Mot de passe :</label>
        <input type="password" class="form-control" id="password" v-model="password" required />
      </div>
      <button type="submit" class="btn btn-primary">Connexion</button>
      <p v-if="wrongPassword" class="error-message">Mauvais mot de passe</p>
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
          // Appeler la fonction authenticate() de QuizApiService
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

<style scoped>
.admin-login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.login-form {
  width: 300px;
  max-width: 100%;
  margin-top: 2rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  font-size: 1.2rem;
  font-weight: bold;
}

.error-message {
  color: black;
  margin-top: 0.5rem;
}

.btn {
  display: inline-block;
  background-color: #0088cc;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary {
  background-color: #0088cc;
}

.btn-primary:hover {
  background-color: #006699;
}

.input {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>
