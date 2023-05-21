<template>
  <div class="admin-questions-list">
    <div class="button-container">
      <button @click="createQuestion" class="create-question-button">Créer une question</button>
    </div>
    <h2 class="questions-title">Liste des questions</h2>
    <ul class="questions-list">
      <li v-for="question in state.questions" :key="question.id" class="question-item">
        <div class="question-container">
          <div class="question-info">
            <h3 class="question-heading">{{ question.position }}. {{ question.title }}</h3>
            <p class="question-text">{{ question.text }}</p>
            <router-link :to="`/admin/question-detail/${question.position}`" class="details-link">Détails</router-link>
          </div>
          <div class="question-photo">
            <img :src="question.photo" alt="Question Photo" class="question-image" />
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.admin-questions-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.create-question-button {
  background-color: #4caf50;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.create-question-button:hover {
  background-color: #45a049;
}

.questions-title {
  font-size: 24px;
  margin-bottom: 20px;
}

.questions-list {
  list-style: none;
  padding: 0;
}

.question-item {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
}

.question-container {
  display: flex;
  align-items: center;
}

.question-info {
  flex: 1;
}

.question-heading {
  font-size: 20px;
  margin-bottom: 10px;
}

.question-text {
  margin-bottom: 10px;
}

.details-link {
  color: #4caf50;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.details-link:hover {
  color: #45a049;
}

.question-photo {
  flex: 0 0 200px;
  margin-left: 20px;
}

.question-image {
  max-width: 100%;
  border-radius: 5px;
}
</style>

<script>
import { useRouter } from "vue-router";
import { reactive, onMounted } from 'vue';
import QuizApiService from '../services/QuizApiService';

export default {
  name: 'AdminQuestionsList',
  setup() {
    const router = useRouter();
    const state = reactive({
      questions: [],
    });

    const fetchQuestions = async () => {
      try {
        const responses = await QuizApiService.getAllQuestions();
        state.questions = responses.data.map(response => ({
          id: response[0],
          position: response[1],
          title: response[2],
          text: response[3],
          photo: response[4],
        }));
      } catch (error) {
        console.error(error);
      }
    };

    const createQuestion = () => {
      // Logic for creating a new question
      router.push('/admin/question-add');
    };

    onMounted(() => {
      fetchQuestions();
    });

    return {
      state,
      createQuestion,
    };
  },
};
</script>
