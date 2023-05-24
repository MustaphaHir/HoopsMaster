<template>
  <div class="question-edit">
    <h2>Édition de la question</h2>

    <form @submit.prevent="submitForm" v-if="question">
      <div class="form-group">
        <label for="position">Position:</label>
        <input type="number" id="position" v-model="question.position" required>
      </div>

      <div class="form-group">
        <label for="title">Titre:</label>
        <input type="text" id="title" v-model="question.title" required>
      </div>

      <div class="form-group">
        <label for="text">Texte :</label>
        <textarea id="text" v-model="question.text" required></textarea>
      </div>

      <div class="form-group">
        <label for="image">Image :</label>
        <input type="file" id="image" @change="handleImageUpload" accept="image/*">
        <div class="image-preview" v-if="imagePreview">
          <img :src="imagePreview" alt="Preview">
        </div>
      </div>

      <h3>Réponses possibles:</h3>
      <ul class="answers-list">
        <li v-for="answer in question.possibleAnswers" :key="answer.id" class="answer-item">
          <div class="answer-text-group">
            <input type="text" v-model="answer.text" required>
          </div>
          <div class="answer-correct-group">
            <label>
              <input type="checkbox" v-model="answer.isCorrect">
              Réponse correcte
            </label>
          </div>
        </li>
      </ul>

      <div class="button-container">
        <button class="save-button" type="submit">Sauvegarder</button>
        <button class="cancel-button" @click.prevent="cancelEdit">Annuler</button>
      </div>
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

<style scoped>
.question-edit {
  padding: 2rem;
}

.question-edit h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-weight: bold;
}

textarea {
  width: 100%;
  min-height: 100px;
  resize: vertical;
}

.image-preview {
  margin-top: 1rem;
}

.image-preview img {
  max-width: 100%;
  max-height: 200px;
}

.answers-list {
  list-style: none;
  padding: 0;
}

.answer-item {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.answer-text-group {
  flex: 1;
  margin-right: 1rem;
}

.answer-correct-group {
  flex-shrink: 0;
}

.button-container {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
}

.save-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #0088cc;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 0.5rem;
}

.cancel-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #cc0000;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
