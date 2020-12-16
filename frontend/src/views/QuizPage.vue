<template>
  <section>
    <router-view></router-view>
  </section>
</template>

<script>

export default {
  name: 'QuizPage',
  components: {
  },

  data() {
    return {
    };
  },

  computed: {
  },

  watch: {
  },

  mounted() {
    this.$store.dispatch('GET_QUIZ_RELATIONSHIP_LIST_FROM_LOCAL_YAML');
  },
};
</script>

<style scoped>
</style>
