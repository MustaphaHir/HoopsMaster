<template>
  <div class="new-quiz-page">
    <h1 class="title">Participation au quiz</h1>
    <form @submit.prevent="launchNewQuiz" class="form">
      <div class="input">
        <input type="text" placeholder="Nom du joueur" id="playerName" v-model="username" required />
      </div>
      <p v-if="wrongUsername" class="error-message">Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.</p>
      <button type="submit" class="start-quiz-button">Commencer le quiz !</button>
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
      wrongUsername: false,
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
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.title {
  font-size: 3rem;
  margin-bottom: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input {
  margin-bottom: 1.5rem;

}

input {
  width: 300px;
  padding: 0.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

label {
  font-size: 1rem;
  font-weight: bold;
}

.error-message {
  color: black;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.start-quiz-button {
  display: inline-block;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background-color: #ff5f58;
  border: none;
  border-radius: 5px;
  text-decoration: none;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.start-quiz-button:hover {
  transform: translateY(-2px);
}
</style>
