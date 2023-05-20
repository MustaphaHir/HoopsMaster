<template>
  <div>
    <h1>Score</h1>
    <h2>Votre score : {{ userScore }} / {{ totalNumberOfQuestions }}</h2>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  data() {
    return {
      userScore: 0, // Variable pour stocker le score de l'utilisateur
      totalNumberOfQuestions: 0
    };
  },
  created() {
    // Appeler une méthode pour récupérer le score de l'utilisateur depuis le service de stockage
    this.fetchUserScore();
  },
  methods: {
    fetchUserScore() {
      // Utiliser ParticipationStorageService ou un service similaire pour récupérer le score de l'utilisateur
      // Exemple :
      this.userScore = participationStorageService.getParticipationScore()
      console.log(this.userScore)
      this.totalNumberOfQuestions = participationStorageService.getTotalNumberOfQuestions()
    },
  },
};
</script>