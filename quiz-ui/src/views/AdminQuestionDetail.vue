<template>
  <div class="admin-question-detail">
    <h2 v-if="question" class="question-title">{{ question.title }}</h2>
    <div v-if="question" class="question-container">
      <img v-if="question.image" :src="question.image" alt="Question Image" class="question-image" />
      <h3 class="question-text">{{ question.text }}</h3>
    </div>

    <ul v-if="question" class="options-list">
      <li v-for="option in question.possibleAnswers" :key="option.id" class="option-item">
        <span class="option-text">{{ option.text }}</span>
        <span v-if="option.isCorrect" class="correct-mark">✅</span>
      </li>
    </ul>

    <div class="button-container">
      <button @click="editQuestion" class="edit-button">Éditer</button>
      <button @click="deleteQuestion" class="delete-button">Supprimer</button>
    </div>
  </div>
</template>

<style scoped>
.admin-question-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.question-title {
  font-size: 24px;
  margin-bottom: 20px;
}

.question-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.question-image {
  max-width: 100%;
  border-radius: 5px;
  margin-bottom: 10px;
}

.question-text {
  font-size: 18px;
}

.options-list {
  list-style: none;
  padding: 0;
  margin-bottom: 20px;
}

.option-item {
  cursor: pointer;
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.option-text {
  margin-right: 10px;
}

.correct-mark {
  color: #4caf50;
  font-size: 18px;
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.edit-button,
.delete-button {
  background-color: #4caf50;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  margin-left: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.edit-button:hover,
.delete-button:hover {
  background-color: #45a049;
}
</style>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import QuizApiService from '../services/QuizApiService';

export default {
  name: 'AdminQuestionDetail',
  setup() {
    const question = ref(null);
    const router = useRouter();
    const questionPosition = router.currentRoute.value.params.id;

    const fetchQuestion = async () => {
      try {
        const response = await QuizApiService.getQuestion(questionPosition);
        question.value = response.data;
      } catch (error) {
        console.error(error);
      }
    };

    const editQuestion = () => {
      router.push(`/admin/question-edit/${questionPosition}`);
    };

    const deleteQuestion = async () => {
      try {
        await QuizApiService.deleteQuestionbyPosition(questionPosition);
        router.push('/admin/questions');
      } catch (error) {
        console.error(error);
      }
    };

    onMounted(() => {
      fetchQuestion();
    });

    return {
      question,
      editQuestion,
      deleteQuestion,
    };
  },
};
</script>
