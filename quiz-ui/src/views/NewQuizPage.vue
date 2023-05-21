<template>
  <div class="new-quiz-page">
    <h1>Participation au quiz</h1>
    <form @submit.prevent="launchNewQuiz">
      <div class="form-group">
        <label for="playerName">Nom du joueur</label>
        <input type="text" class="form-control" id="playerName" v-model="username" required />
        <p v-if="wrongUsername" class="error-message">Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.
        </p>
      </div>
      <button type="submit" class="btn btn-primary">Commencer le quiz</button>
    </form>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  data() {
    return {
      username: "",
      wrongUsername: false
    };
  },
  methods: {
    async launchNewQuiz() {
      const isUsernameTaken = await quizApiService.checkUsername(this.username);

      if (isUsernameTaken.status === 200 && isUsernameTaken.data.data === true) {
        this.wrongUsername = true;
        return;
      }

      participationStorageService.savePlayerName(this.username);

      this.$router.push('/questions');
    },
  },
};
</script>

<style scoped>
.new-quiz-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  font-weight: bold;
}

input[type="text"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.error-message {
  color: #ff5252;
  margin-top: 10px;
}

.btn-primary {
  background-color: #ff5252;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #ff1744;
}
</style>
