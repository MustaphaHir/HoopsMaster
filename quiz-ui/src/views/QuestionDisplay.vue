<template>
  <div>
    <h2 v-if="question">{{ question.data.title }}</h2>
    <img v-if="question && question.data.image" :src="question.data.image" />
    <h3 v-if="question">{{ question.data.text }}</h3>

    <ul v-if="question">
      <li v-for="option in question.data.possibleAnswers" :key="option.id" @click="selectOption(option)">
        {{ option.text }}
      </li>
    </ul>
  </div>
</template>


<script>
export default {
  name: "QuestionDisplay",
  props: {
    question: {
      type: Object,
      required: true,
    }
  },

  emits: ['answer-selected'], // Déclaration de l'événement émis

  methods: {
    selectOption(option) {
      this.$emit("answer-selected", option.id);
    }
  }
};
</script>
