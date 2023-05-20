<template>
  <div>
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
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
      userAnswerPositions: []
    };
  },
  created() {
    this.initializeQuiz();
  },
  methods: {
    async initializeQuiz() {
      const quizInfo = await QuizApiService.getQuizInfo();
      this.totalNumberOfQuestions = quizInfo.data.size;
      participationStorageService.saveTotalNumberOfQuestions(this.totalNumberOfQuestions)
      await this.loadQuestionByPosition(this.currentQuestionPosition);
    },
    async loadQuestionByPosition(position) {
      const question = await QuizApiService.getQuestion(position);
      this.currentQuestion = question;
      this.currentQuestionPosition = position;
    },
    async answerClickedHandler(option) {
      if (option % 4 == 0) {
        option = 4
        this.userAnswerPositions.push(option)
      }
      else {
        this.userAnswerPositions.push(option % 4)
      }
      console.log(this.userAnswerPositions)

      if (this.currentQuestionPosition < this.totalNumberOfQuestions) {
        this.loadQuestionByPosition(this.currentQuestionPosition + 1);
      } else {
        this.endQuiz();
      }
    },
    async submitQuiz() {
      const participantData = {
        // Récupérer les informations du participant (nom, réponses, etc.)
        // et les formater correctement pour l'envoi au serveur
        playerName: participationStorageService.getPlayerName(),
        answers: this.userAnswerPositions,
      };

      try {
        const response = await QuizApiService.addParticipant(participantData);
        console.log("Participant ajouté :", response.data);
        participationStorageService.saveParticipationScore(response.data.score)
        // Traiter la réponse du serveur, afficher un message de confirmation, etc.
      } catch (error) {
        console.error("Erreur lors de l'ajout du participant :", error);
        // Gérer l'erreur, afficher un message d'erreur, etc.
      }
    },
    async endQuiz() {
      // Enregistrement des réponses ou traitement ultérieur
      console.log("Responses:", this.userAnswerPositions);

      await this.submitQuiz();



      // Émettre un événement vers le composant parent (QuestionsPage) pour indiquer la fin du quiz
      this.$emit('quiz-ended');

      this.$router.push('/score')
    }
  }
};
</script>
