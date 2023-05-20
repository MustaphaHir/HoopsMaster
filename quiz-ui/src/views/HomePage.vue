<template>
  <div>
    <h1>Home page</h1>
    <div v-for="scoreEntry in registeredScores" :key="scoreEntry.date">
      {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
    </div>
    <RouterLink to="/new-quiz">Démarrer le quiz !</RouterLink>
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
