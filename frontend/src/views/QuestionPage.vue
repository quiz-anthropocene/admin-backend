<template>
  <section>
    <router-view></router-view>
  </section>
</template>

<script>

export default {
  name: 'QuestionPage',
  components: {
  },

  data() {
    return {
    };
  },

  computed: {
    questions() {
      return this.$store.state.questions;
    },
  },

  watch: {
    // eslint-disable-next-line
    questions (newQuestions, oldQuestions) {
      this.$store.dispatch('UPDATE_QUESTION_FILTERS');
    },
  },

  mounted() {
    if (this.questions) {
      this.$store.dispatch('UPDATE_QUESTION_FILTERS');
    }
  },
};
</script>

<style scoped>
</style>
