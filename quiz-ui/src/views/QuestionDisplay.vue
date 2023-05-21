<template>
  <div class="question-display">
    <div class="question-header">
      <h2 v-if="question">{{ question.data.title }}</h2>
      <img v-if="question && question.data.image" :src="question.data.image" />
      <h3 v-if="question">{{ question.data.text }}</h3>
    </div>

    <ul v-if="question" class="answers-list">
      <li v-for="option in question.data.possibleAnswers" :key="option.id" class="answer-item">
        <label>
          <input type="radio" v-model="selectedOption" :value="option.id" class="answer-input" />
          <span class="answer-text">{{ option.text }}</span>
        </label>
      </li>
    </ul>

    <button @click="nextQuestion" class="next-button">Question suivante</button>
  </div>
</template>

<script>
export default {
  name: "QuestionDisplay",
  props: {
    question: {
      type: Object,
      required: true,
    },
  },
  emits: ['answer-selected'],

  data() {
    return {
      selectedOption: null,
    };
  },

  methods: {
    nextQuestion() {
      if (this.selectedOption !== null) {
        this.$emit('answer-selected', this.selectedOption);
        this.selectedOption = null;
      }
    }
  },
};
</script>

<style scoped>
.question-display {
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
}

.question-header {
  margin-bottom: 20px;
}

h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

img {
  max-width: 80%;
  margin-bottom: 15px;
}

h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.answers-list {
  list-style: none;
  padding: 0;
  margin-bottom: 20px;
}

.answer-item {
  margin-bottom: 10px;
}

.answer-input {
  margin-right: 10px;
}

.answer-text {
  font-size: 16px;
}

.next-button {
  background-color: #ff5252;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.next-button:hover {
  background-color: #ff1744;
}
</style>
