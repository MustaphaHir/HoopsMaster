<template>
  <div class="home-page">
    <img alt="Vue logo" class="logo" src="@/assets/logo_hoops_master.png" />

    <div class="score-container">
      <h2>Meilleurs scores 🏆</h2>
      <div v-for="scoreEntry in registeredScores" :key="scoreEntry.date" class="score-entry">
        <span class="player-name">{{ scoreEntry.playerName }}</span>
        <span class="score">{{ scoreEntry.score }}</span>
      </div>
    </div>

    <div class="quiz-area">
      <h1>Es-tu prêt ?</h1>
      <RouterLink to="/new-quiz" class="start-quiz-button">Démarrer le quiz !</RouterLink>
    </div>
  </div>
</template>

<script>
import { RouterLink } from "vue-router";
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  components: {
    RouterLink,
  },
  data() {
    return {
      registeredScores: [],
    };
  },
  async created() {
    try {
      const response = await quizApiService.getQuizInfo();
      this.registeredScores = response.data.scores;
      console.log("Composant Home page 'created'");
    } catch (error) {
      console.error(error);
    }
  },
};
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  text-align: center;
}

.score-container {
  margin-top: 3rem;
}

.score-entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #f2f2f2;
  color: #333;
  border-radius: 5px;
}

.player-name {
  font-weight: bold;
}

.quiz-area {
  margin-top: 3rem;
}

.start-quiz-button {
  display: inline-block;
  padding: 1rem 2rem;
  font-size: 1.5rem;
  font-weight: bold;
  color: #fff;
  background-color: #ff5f58;
  border-radius: 5px;
  text-decoration: none;
  transition: transform 0.3s ease;
}

.start-quiz-button:hover {
  transform: translateY(-2px);
}
</style>
