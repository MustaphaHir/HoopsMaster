<template>
  <div class="home-page">
    <h1 class="title">Hoops Master Quiz</h1>
    <div class="scoreboard">
      <h2 class="scoreboard-title">Meilleurs scores</h2>
      <div v-for="scoreEntry in registeredScores" :key="scoreEntry.date" class="score-entry">
        <span class="player-name">{{ scoreEntry.playerName }}</span>
        <span class="score">{{ scoreEntry.score }}</span>
      </div>

    </div>

    <RouterLink to="/new-quiz" class="start-quiz-button">Démarrer le quiz !</RouterLink>
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
}

.title {
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
}

.scoreboard {
  width: 300px;
  background-color: #f2f2f2;
  padding: 1rem;
  border-radius: 5px;
  margin-bottom: 2rem;
}

.scoreboard-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.score-entry {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.player-name {
  font-weight: bold;
}

.score {
  font-weight: bold;
}

.start-quiz-button {
  padding: 0.8rem 2rem;
  background-color: #0088cc;
  color: #fff;
  font-size: 1rem;
  text-decoration: none;
  border-radius: 5px;
}

.start-quiz-button:hover {
  background-color: #006699;
}
</style>
