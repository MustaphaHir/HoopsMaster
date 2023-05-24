<template>
  <div class="question-display">
    <div class="question-header">
      <h2 v-if="question">{{ question.data.title }}</h2>
      <img v-if="question && question.data.image" :src="question.data.image" />
      <h3 v-if="question">{{ question.data.text }}</h3>
    </div>
    <div class="radio-input">
      <ul v-if="question" class="answers-list">
        <li v-for="option in question.data.possibleAnswers" :key="option.id" class="answer-item">

          <label class="checkbox-container">
            <input type="radio" v-model="selectedOption" :value="option.id" class="input" />
            <span class="checkmark"></span>
            <span class="answer-text">{{ option.text }}</span>
          </label>

        </li>
      </ul>
    </div>
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
.checkbox-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  padding-right: 30px;
  margin-bottom: 8px;
  cursor: pointer;
  font-size: 16px;
}

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
  font-size: 25px;
  margin-bottom: 10px;
}

.answers-list {
  list-style: none;
  padding: 0;
  margin-bottom: 20px;
}

.answer-item {
  margin-bottom: 10px;
  font-size: 25px;
}

.answer-input {
  margin-right: 10px;
}

.answer-text {
  font-size: 25px;
  margin-left: 13px;
}


.input {
  -webkit-appearance: none;
  /* remove default */
  display: block;
  margin: 10px;
  width: 24px;
  height: 24px;
  border-radius: 12px;
  cursor: pointer;
  vertical-align: middle;
  box-shadow: hsla(0, 0%, 100%, .15) 0 1px 1px, inset hsla(0, 0%, 0%, .5) 0 0 0 1px;
  background-color: hsla(0, 0%, 0%, .2);
  background-image: -webkit-radial-gradient(hsla(200, 100%, 90%, 1) 0%, rgb(224, 17, 17) 15%, rgb(224, 17, 17) 28%, rgb(224, 17, 17) 70%);
  background-repeat: no-repeat;
  -webkit-transition: background-position .15s cubic-bezier(.8, 0, 1, 1),
    -webkit-transform .25s cubic-bezier(.8, 0, 1, 1);
  outline: none;
}



.input:active {
  -webkit-transform: scale(1.5);
  -webkit-transition: -webkit-transform .1s cubic-bezier(0, 0, .2, 1);
}



/* The up/down direction logic */

.input,
.input:active {
  background-position: 0 24px;
}

.input:checked {
  background-position: 0 0;
}

.input:checked~.input,
.input:checked~.input:active {
  background-position: 0 -24px;
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