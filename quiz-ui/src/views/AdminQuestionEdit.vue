<template>
  <div>
    <h2>Édition de la question</h2>

    <form @submit.prevent="submitForm" v-if="question">
      <label for="position">Position:</label>
      <input type="number" id="position" v-model="question.position" required>

      <label for="title">Titre:</label>
      <input type="text" id="title" v-model="question.title" required>

      <label for="text">Intitulés:</label>
      <textarea id="text" v-model="question.text" required></textarea>

      <label for="image">Images:</label>
      <input type="file" id="image" @change="handleImageUpload" accept="image/*">
      <img v-if="imagePreview" :src="imagePreview" alt="Preview">

      <h3>Réponses possibles:</h3>
      <ul>
        <li v-for="answer in question.possibleAnswers" :key="answer.id">
          <input type="text" v-model="answer.text" required>
          <label>
            <input type="checkbox" v-model="answer.isCorrect">
            Réponse correcte
          </label>
        </li>
      </ul>

      <button type="submit">Sauvegarder</button>
      <button @click.prevent="cancelEdit">Annuler</button>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import QuizApiService from '../services/QuizApiService';

export default {
  name: 'AdminQuestionEdit',
  setup() {
    const router = useRouter();
    const questionPosition = router.currentRoute.value.params.id;
    const question = ref(null);
    const imagePreview = ref(null);

    const fetchQuestion = async () => {
      try {
        const response = await QuizApiService.getQuestion(questionPosition);
        question.value = response.data;
      } catch (error) {
        console.error(error);
      }
    };

    const saveQuestion = async () => {
      try {
        const updatedQuestion = {
          position: question.value.position,
          title: question.value.title,
          text: question.value.text,
          image: question.value.image,
          possibleAnswers: question.value.possibleAnswers,
        };

        await QuizApiService.updateQuestion(questionPosition, updatedQuestion);
        router.push('/admin/questions');
      } catch (error) {
        console.error(error);
      }
    };

    const cancelEdit = () => {
      router.push('/admin/questions');
    };

    const submitForm = () => {
      saveQuestion();
    };

    const handleImageUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        // You can perform additional checks here before uploading the file
        // For example, check the file type, size, etc.
        // Then, upload the file to the server or store it in the desired format
        // In this example, we'll simply set the imagePreview ref to the image URL
        const reader = new FileReader();
        reader.onload = () => {
          imagePreview.value = reader.result;
          question.value.image = reader.result;
        };
        reader.readAsDataURL(file);
      }
    };

    onMounted(() => {
      fetchQuestion();
    });

    return {
      question,
      imagePreview,
      submitForm,
      cancelEdit,
      handleImageUpload,
    };
  },
};
</script>
