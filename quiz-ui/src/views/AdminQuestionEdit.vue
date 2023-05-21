<template>
  <div class="question-edit">
    <h2>Édition de la question</h2>

    <form @submit.prevent="submitForm" v-if="question">
      <label for="position">Position:</label>
      <input type="number" id="position" v-model="question.position" required>

      <label for="title">Titre:</label>
      <input type="text" id="title" v-model="question.title" required>

      <label for="text">Texte :</label>
      <textarea id="text" v-model="question.text" required></textarea>

      <label for="image">Image :</label>
      <input type="file" id="image" @change="handleImageUpload" accept="image/*">
      <div class="image-preview" v-if="imagePreview">
        <img :src="imagePreview" alt="Preview">
      </div>

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

      <div class="buttons">
        <button class="save-button" type="submit">Sauvegarder</button>
        <button class="cancel-button" @click.prevent="cancelEdit">Annuler</button>
      </div>
    </form>
  </div>
</template>

<style>
.question-edit {
  padding: 20px;
}

h2 {
  color: #ff5252;
  font-size: 24px;
  margin-bottom: 20px;
}

form {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

label {
  font-weight: bold;
}

input[type="number"],
input[type="text"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 10px;
}

.image-preview {
  margin-bottom: 20px;
}

.image-preview img {
  max-width: 50%;
}

h3 {
  color: #4caf50;
  font-size: 18px;
  margin-bottom: 10px;
}

ul {
  list-style-type: none;
  padding: 0;
  margin-bottom: 20px;
}

li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

li input[type="text"] {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

li label {
  margin-left: 10px;
}

.buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.save-button {
  background-color: #4caf50;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  margin-right: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cancel-button {
  background-color: #ffffff;
  color: #4caf50;
  border: 1px solid #4caf50;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-button:hover,
.cancel-button:hover {
  background-color: #4caf50;
  color: #ffffff;
}

@keyframes fade-in {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

.fade-in {
  animation: fade-in 0.5s ease;
}
</style>

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
