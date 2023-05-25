<template>
  <div>
    <h1 class="question-title">Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    <h2 :class="['remaining-time', remainingTime <= 10 ? 'warning-animation' : '']">⏱️ {{ formatRemainingTime() }}
      restantes</h2>

    <QuestionDisplay v-if="currentQuestion" :question="currentQuestion" @answer-selected="answerClickedHandler" />
  </div>
</template>

<script>
import QuestionDisplay from './QuestionDisplay.vue';
import QuizApiService from '@/services/QuizApiService';
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: 'QuestionsManager',
  components: {
    QuestionDisplay
  },
  data() {
    return {
      currentQuestionPosition: 1,
      totalNumberOfQuestions: 0,
      currentQuestion: null,
      userAnswerPositions: [],
      remainingTime: 60,
      timerRunning: false,
      timer: null,
    };
  },
  created() {
    this.initializeQuiz();
  },
  methods: {
    async initializeQuiz() {
      const quizInfo = await QuizApiService.getQuizInfo();
      this.totalNumberOfQuestions = quizInfo.data.size;
      participationStorageService.saveTotalNumberOfQuestions(this.totalNumberOfQuestions);
      await this.loadQuestionByPosition(this.currentQuestionPosition);
      this.startTimer();
    },
    async loadQuestionByPosition(position) {
      const question = await QuizApiService.getQuestion(position);
      this.currentQuestion = question;
      this.currentQuestionPosition = position;
      this.remainingTime = 60;
    },
    async answerClickedHandler(option) {
      if (option % 4 === 0) {
        option = 4;
        this.userAnswerPositions.push(option);
      } else {
        this.userAnswerPositions.push(option % 4);
      }
      console.log(this.userAnswerPositions);

      const currentQuestionPosition = this.currentQuestionPosition;

      if (currentQuestionPosition < this.totalNumberOfQuestions) {
        if (this.remainingTime <= 0) {
          this.userAnswerPositions.push(0);
        }

        await this.loadQuestionByPosition(currentQuestionPosition + 1);

        if (currentQuestionPosition === this.currentQuestionPosition) {
          this.startTimer();
        }
      } else {
        this.endQuiz();
      }
    },

    async submitQuiz() {
      const participantData = {
        playerName: participationStorageService.getPlayerName(),
        answers: this.userAnswerPositions,
      };

      try {
        const response = await QuizApiService.addParticipant(participantData);
        if (response && response.data) {
          console.log("Participant ajouté :", response.data);
          participationStorageService.saveParticipationScore(response.data.score);
        } else {
          console.error("Réponse du serveur invalide :", response);
        }
      } catch (error) {
        console.error("Erreur lors de l'ajout du participant :", error);
      }
    },
    startTimer() {
      this.timerRunning = true;
      this.timer = setInterval(() => {
        this.remainingTime--;

        if (this.remainingTime <= 0) {
          clearInterval(this.timer);
          this.userAnswerPositions.push(0);
          this.nextQuestion();
        }
      }, 1000);
    },
    async endQuiz() {
      console.log("Responses:", this.userAnswerPositions);
      await this.submitQuiz();
      this.$emit('quiz-ended');
      this.$router.push('/score');
    },
    nextQuestion() {
      if (this.currentQuestionPosition < this.totalNumberOfQuestions) {
        clearInterval(this.timer);
        this.loadQuestionByPosition(this.currentQuestionPosition + 1);
        this.startTimer();
      } else {
        this.endQuiz();
      }
    },
    formatRemainingTime() {
      const minutes = Math.floor(this.remainingTime / 60);
      const seconds = this.remainingTime % 60;
      return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    },
  }
};
</script>

<style scoped>
.question-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

.remaining-time {
  font-size: 36px;
  color: #ff5252;
  margin-bottom: 20px;
  transition: color 0.5s ease-in-out;
}

.remaining-time.warning {
  color: #ff1744;
}


.warning-animation {
  animation: pulse 0.5s infinite alternate;
}

@keyframes pulse {
  0% {
    color: #ff5252;
  }

  100% {
    color: #ffffff;
    text-shadow: 0 0 5px #ff5252, 0 0 10px #ff5252;
  }
}
</style>