<template>
  <div class="score-page">
    <h1 class="title">Score</h1>
    <div class="score-card">
      <div class="score-info">
        <h2 class="score-label">Votre score :</h2>
        <h2 class="score-value">{{ userScore }} / {{ totalNumberOfQuestions }}</h2>
      </div>
      <div class="percentage-info">
        <h3 class="percentage-label">Vous êtes meilleur que :</h3>
        <h3 class="percentage-value">{{ userScorePercentage }} % des autres joueurs</h3>
      </div>
    </div>
    <div class="basketball-animation">
      <div v-for="index in numberOfBalloons" :key="index" class="basketball-balloon"></div>
    </div>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
import QuizApiService from "../services/QuizApiService";

export default {
  data() {
    return {
      userScore: 0,
      totalNumberOfQuestions: 0,
      userScorePercentage: 0,
      numberOfBalloons: 10, // Nombre de ballons de basket à afficher
    };
  },
  created() {
    this.fetchUserScore();
  },
  methods: {
    fetchUserScore() {
      this.userScore = participationStorageService.getParticipationScore();
      this.totalNumberOfQuestions = participationStorageService.getTotalNumberOfQuestions();
      QuizApiService.getPercentageScore(this.userScore)
        .then(response => {
          this.userScorePercentage = Math.round(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
.score-page {
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

.score-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f2f2f2;
  padding: 2rem;
  border-radius: 5px;
}

.score-info,
.percentage-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}

.score-label,
.percentage-label {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  text-align: center;
}

.score-value,
.percentage-value {
  font-size: 2rem;
  font-weight: bold;
  color: #0088cc;
}

.basketball-animation {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.basketball-balloon {
  background-image: url('@/assets/basket.png');
  /* Remplacez par le chemin de votre image de ballon de basket */
  background-size: cover;
  width: 80px;
  height: 80px;
  margin: 0.5rem;
  animation: balloon-appear 1s ease-in-out both;
}

@keyframes balloon-appear {
  0% {
    opacity: 0;
    transform: translateY(50px) scale(0.5);
  }

  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
