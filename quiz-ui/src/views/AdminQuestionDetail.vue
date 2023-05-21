<template>
  <div>
    <h2 v-if="question">{{ question.title }}</h2>
    <img v-if="question && question.image" :src="question.image" />
    <h3 v-if="question">{{ question.text }}</h3>

    <ul v-if="question">
      <li v-for="option in question.possibleAnswers" :key="option.id" @click="selectOption(option)">
        {{ option.text }}
        <span v-if="option.isCorrect">✅</span>
      </li>
    </ul>

    <button @click="editQuestion">Éditer</button>
    <button @click="deleteQuestion">Supprimer</button>
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
