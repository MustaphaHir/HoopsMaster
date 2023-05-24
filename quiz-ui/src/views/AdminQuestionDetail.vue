<template>
  <div class="admin-question-detail">
    <div v-if="question" class="question-section">
      <h2 class="question-title">{{ question.position }} - {{ question.title }}</h2>
    </div>

    <div v-if="question" class="question-section">
      <div class="question-container">
        <img v-if="question.image" :src="question.image" alt="Question Image" class="question-image" />
        <p class="question-text">{{ question.text }}</p>
      </div>
    </div>

    <div v-if="question" class="question-section">
      <div class="options-list">
        <div v-for="option in question.possibleAnswers" :key="option.id" class="option-item">
          <span class="option-text">{{ option.text }}</span>
          <span v-if="option.isCorrect" class="correct-mark"> ✅</span>
        </div>
      </div>
    </div>

    <div class="button-container">
      <button @click="editQuestion" class="edit-button">Éditer</button>
      <button @click="deleteQuestion" class="delete-button">Supprimer</button>
    </div>
  </div>
</template>

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

<style scoped>
.admin-question-detail {
  padding: 2rem;
}

.question-section {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.question-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.question-container {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.question-image {
  width: 150px;
  height: auto;
  margin-right: 1rem;
}

.question-text {
  font-size: 1.2rem;
}

.options-list {
  margin-bottom: 2rem;
}

.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.option-text {
  margin-left: 0.5rem;
  font-size: 1.2rem;
}

.correct-mark {
  color: green;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.edit-button,
.delete-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #0088cc;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 0.5rem;
}

.delete-button {
  background-color: #cc0000;
}
</style>
