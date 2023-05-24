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
      <li v-if="state.questions.length === 0" class="empty-list-message">Aucune question disponible</li>
    </ul>
  </div>
</template>



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



<style scoped>
.admin-questions-list {
  padding: 2rem;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.create-question-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #0088cc;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.questions-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.questions-list {
  list-style: none;
  padding: 0;
}

.question-item {
  margin-bottom: 2rem;
  border: 1px solid #dddddd;
  border-radius: 5px;
  padding: 1rem;
}


.question-container {
  display: flex;
}

.question-info {
  flex: 1;
}

.question-heading {
  font-size: 1.2rem;
  font-weight: bold;
}

.question-text {
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

.details-link {
  display: inline-block;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #0088cc;
  color: #ffffff;
  text-decoration: none;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.question-photo {
  flex: 0 0 100px;
  margin-left: 1rem;
}

.question-image {
  width: 100%;
  height: auto;
}

.empty-list-message {
  margin-top: 2rem;
  font-style: italic;
  text-align: center;
  color: #808080;
}
</style>