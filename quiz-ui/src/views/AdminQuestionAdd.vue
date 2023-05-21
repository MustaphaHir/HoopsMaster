<template>
  <div>
    <h2>Ajout d'une nouvelle question</h2>

    <form @submit.prevent="submitForm" v-if="question">
      <label for="position">Position:</label>
      <input type="number" id="position" v-model="question.position" required>

      <label for="title">Titre:</label>
      <input type="text" id="title" v-model="question.title" required>

      <label for="text">Intitulé:</label>
      <textarea id="text" v-model="question.text" required></textarea>

      <label for="image">Image:</label>
      <input type="file" id="image" @change="handleImageUpload" accept="image/*">
      <img v-if="imagePreview" :src="imagePreview" alt="Preview">

      <h3>Réponses possibles:</h3>
      <ul>
        <li v-for="answer in question.possibleAnswers" :key="answer.id">
          <input type="text" v-model="answer.text" required>
          <label>
            <input type="radio" :value="answer.id" v-model="question.correctAnswerId">
            Réponse correcte
          </label>
        </li>
      </ul>

      <button type="submit">Ajouter</button>
      <button @click.prevent="cancelAdd">Annuler</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import QuizApiService from '../services/QuizApiService';

export default {
  name: 'AdminQuestionAdd',
  setup() {
    const router = useRouter();
    const question = ref({
      position: null,
      title: '',
      text: '',
      image: null,
      possibleAnswers: [
        { id: 1, text: '', isCorrect: false },
        { id: 2, text: '', isCorrect: false },
        { id: 3, text: '', isCorrect: false },
        { id: 4, text: '', isCorrect: false },
      ],
      correctAnswerId: null,
    });
    const imagePreview = ref(null);

    const saveQuestion = async () => {
      try {
        const newQuestion = {
          position: question.value.position,
          title: question.value.title,
          text: question.value.text,
          image: question.value.image,
          possibleAnswers: question.value.possibleAnswers.map(answer => ({
            ...answer,
            isCorrect: answer.id === question.value.correctAnswerId
          })),
          correctAnswerId: question.value.correctAnswerId,
        };

        await QuizApiService.addQuestion(newQuestion);
        router.push('/admin/questions');
      } catch (error) {
        console.error(error);
      }
    };

    const cancelAdd = () => {
      router.push('/admin/questions');
    };

    const submitForm = () => {
      saveQuestion();
    };

    const handleImageUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          imagePreview.value = reader.result;
          question.value.image = reader.result;
        };
        reader.readAsDataURL(file);
      }
    };

    return {
      question,
      imagePreview,
      submitForm,
      cancelAdd,
      handleImageUpload,
    };
  },
};
</script>
