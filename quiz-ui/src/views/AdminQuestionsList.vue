<template>
  <div>
    <button @click="createQuestion">Créer une question</button>
    <h2>Liste des questions</h2>
    <ul>
      <li v-for="question in state.questions" :key="question.id">
        <div class="question-container">
          <div class="question-info">
            <h3>{{ question.position }}. {{ question.title }}</h3>
            <p>{{ question.text }}</p>
          </div>
          <div class="question-photo">
            <img :src="question.photo" alt="Question Photo" />
            <router-link :to="`/admin/question-detail/${question.position}`">Détails</router-link>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style>
.question-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.question-info {
  flex: 1;
}

.question-photo {
  flex: 0 0 200px;
  margin-left: 20px;
}

.question-photo img {
  max-width: 100%;
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
