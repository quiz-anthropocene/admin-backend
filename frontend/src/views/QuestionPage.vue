<template>
  <section>
    <QuestionFilter />
    <router-view></router-view>
  </section>
</template>

<script>
import QuestionFilter from '../components/QuestionFilter.vue'
// import QuestionPreviewCard from '../components/QuestionPreviewCard.vue'
// import DifficultyBadge from '../components/DifficultyBadge.vue'
// import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'QuestionPage',
  components: {
    QuestionFilter,
    // QuestionPreviewCard,
    // DifficultyBadge,
    // HomeLink
  },

  // data () {
  // },

  computed: {
    questions () {
      return this.$store.state.questions;
    },
    // categories () {
    //   return this.$store.state.categories;
    // },
    // tags () {
    //   return this.$store.state.tags;
    // },
    // authors () {
    //   return this.$store.state.authors;
    // },
    // difficultyLevels () {
    //   return this.$store.state.difficultyLevels;
    // }
  },

  watch: {
    // eslint-disable-next-line
    questions (newQuestions, oldQuestions) {
      console.log("questionPage watch", oldQuestions, newQuestions)
      // this.questionsDisplayed = newQuestions;
      this.$store.dispatch('UPDATE_QUESTION_FILTERS');
    }
  },

  mounted () {
    console.log("questionPage mounted");
    if (this.questions) {
      this.$store.dispatch('UPDATE_QUESTION_FILTERS');
    }
  },

  methods: {
  }
}
</script>

<style scoped>
.row-item-question {
  height: 150px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.1s;
  border: 2px solid var(--primary);
  border-radius: 5px;
  cursor: pointer;
}

@media(hover: hover) and (pointer: fine) {
  .row-item-question:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
}
</style>
