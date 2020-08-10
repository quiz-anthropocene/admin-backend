<template>
  <section class="filter-box">

    <!-- Header -->
    <div class="filter-box--header">
      <div class="row no-gutters">
        <div class="col-6">
          <span class="label label-hidden">
            <span>⚙️&nbsp;<strong>Filtres</strong></span>
          </span>
          <span v-for="(value, key) in quizFilters" :key="key">
            <span v-if="(key === 'tag') && value" class="label label-tag">🏷️{{ value }}</span>
          </span>
        </div>
        <div class="col-6 text-align-right">
          <button v-if="quizFilters.tag" class="btn btn-sm btn-outline-secondary margin-5" @click="clearQuizFilters()">Réinitialiser</button>
          <span v-on:click.stop>
            <router-link class="no-decoration" :to="{ name: 'quiz-list' }">
              <span class="label label-hidden"><strong>{{ quizzesDisplayedCount }}</strong> Quiz</span>
            </router-link>
          </span>
        </div>
      </div>
    </div>

  </section>
</template>

<script>
export default {
  name: 'QuizFilter',
  props: {
  },
  components: {
  },

  data() {
    return {
      tempQuizFilters: {
        tag: null,
      },
      showFilterBox: false,
    };
  },

  computed: {
    quizFilters() {
      return this.$store.state.quizFilters;
    },
    quizzesDisplayedCount() {
      return this.$store.state.quizzesDisplayed.length;
    },
  },

  mounted() {
    if (Object.keys(this.$route.query).length) {
      Object.keys(this.$route.query).forEach((key) => {
        if (this.$route.query[key] !== null) {
          this.tempQuizFilters[key] = this.$route.query[key];
        }
      });
      this.updateQuizFilters();
    }
  },

  methods: {
    clearQuizFilters() {
      this.tempQuizFilters = {
        tag: null,
      };
      this.updateQuizFilters();
    },
    updateQuizFilters() {
      this.$store.dispatch('UPDATE_QUIZ_FILTERS', this.tempQuizFilters);
    },
  },
};
</script>

<style scoped>
.filter-box {
  /* background-color: #ebebeb; */
  box-shadow: 0px 0px 5px 5px #c5c5c5;
  border-radius: 5px;
  margin: 10px 0px;
  padding: 5px;
}
.filter-box > .filter-box--header {
  text-align: left;
  /* cursor: pointer; */
}
</style>
