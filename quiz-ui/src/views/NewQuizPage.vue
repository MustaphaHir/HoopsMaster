<template>
  <div>
    <h1>Participation au quiz</h1>
    <form>
      <div class="mb-3">
        <label for="playerName" class="form-label">Nom du joueur</label>
        <input type="text" class="form-control" id="playerName" v-model="username" />
      </div>
      <button type="button" class="btn btn-primary" @click="launchNewQuiz">Commencer le quiz</button>
    </form>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  data() {
    return {
      username: '',
    };
  },
  methods: {
    launchNewQuiz() {
      participationStorageService.savePlayerName(this.username);
      console.log("Launch new quiz with", this.username);
      // Redirection vers la première question du quiz
      this.$router.push('/questions');
    },
  },
};
</script>

<style>
/* Styles CSS spécifiques à la page NewQuizPage */
</style>
