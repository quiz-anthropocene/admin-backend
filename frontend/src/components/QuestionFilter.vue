<template>
  <section class="filter-box" :class="{ 'background-color-dark-grey': showFilterBox }">

    <!-- Header -->
    <div class="filter-box--header" :class="{ 'padding-bottom-5': showFilterBox }" @click="toggleFilterBox()">
      <div class="row no-gutters">
        <div class="col-8">
          <span class="label label-hidden">
            <span>⚙️&nbsp;<strong>Filtres</strong></span>
            <span v-if="!showFilterBox">&nbsp;▸</span> <!-- ▲ ► -->
            <span v-if="showFilterBox">&nbsp;▾</span> <!-- ▼ -->
          </span>
          <span v-for="(value, key) in questionFilters" :key="key">
            <span v-if="(key === 'category') && value" class="label label-category">📂{{ value }}</span>
            <span v-if="(key === 'tag') && value" class="label label-tag">🏷️{{ value }}</span>
            <span v-if="(key === 'author') && value" class="label label-author">📝{{ value }}</span>
            <span v-if="(key === 'difficulty') && Number.isInteger(value)" class="label label-difficulty"><DifficultyBadge v-bind:difficulty="value" /></span>
          </span>
        </div>
        <div class="col-4 text-align-right" v-on:click.stop>
          <button v-if="questionFilters.category || questionFilters.tag || questionFilters.author || questionFilters.difficulty" class="btn btn-sm btn-outline-secondary margin-5" @click="clearQuestionFilters()">Réinitialiser</button>
          <span class="label label-hidden"><strong>{{ counter }}</strong> {{ objectType }}{{ (objectType === 'question' && questionsDisplayedCount > 1) ? 's' : '' }}</span>
        </div>
      </div>
    </div>

    <!-- Content -->
    <section v-if="showFilterBox" class="filter-box--content">

      <div v-if="categories && objectType =='question'">
        <h3>📂&nbsp;Catégories</h3>
        <FilterLabel v-for="category in categories" :key="category.name" @filter-label-clicked="updateTempQuestionFilter"
          filterType="category" v-bind:filterValue="category.name" v-bind:filterCount="category[objectType === 'question' ? 'question_count' : 'quiz_count']" v-bind:customClass="(category.name === tempQuestionFilters['category']) ? 'label-category--active' : ''" />
      </div>

      <hr class="custom-separator" />

      <div v-if="tags">
        <h3>🏷️&nbsp;Tags</h3>
        <FilterLabel v-for="tag in tags" :key="tag.name" @filter-label-clicked="updateTempQuestionFilter"
          filterType="tag" v-bind:filterValue="tag.name" v-bind:filterCount="tag[objectType === 'question' ? 'question_count' : 'quiz_count']" v-bind:customClass="(tag.name === tempQuestionFilters['tag']) ? 'label-tag--active' : ''" />
      </div>

      <hr class="custom-separator" />

      <div v-if="authors ">
        <h3>📝&nbsp;Auteurs</h3>
        <FilterLabel v-for="author in authors" :key="author.name" @filter-label-clicked="updateTempQuestionFilter"
          filterType="author" v-bind:filterValue="author.name" v-bind:filterCount="author[objectType === 'question' ? 'question_count' : 'quiz_count']" v-bind:customClass="(author.name === tempQuestionFilters['author']) ? 'label-author--active' : ''" />
      </div>

      <hr class="custom-separator" />

      <div v-if="difficultyLevels && objectType =='question'">
        <h3>🏆&nbsp;Difficultés</h3>
        <FilterLabel v-for="difficulty in difficultyLevels" :key="difficulty.name" @filter-label-clicked="updateTempQuestionFilter"
          filterType="difficulty" v-bind:filterValue="difficulty.name" v-bind:filterCount="difficulty[objectType === 'question' ? 'question_count' : 'quiz_count']" v-bind:customClass="(difficulty.value === tempQuestionFilters['difficulty']) ? 'label-difficulty--active' : ''" />
      </div>

      <br />
    </section>

    <!-- Action Buttons -->
    <section v-if="showFilterBox" class="filter-box--action">
      <button class="btn btn-outline-secondary margin-5" @click="clearQuestionFilters()">Réinitialiser</button>
      <button class="btn btn-outline-dark margin-5" @click="toggleFilterBox()">Annuler</button>
      <button class="btn margin-5" :class="JSON.stringify(questionFilters) === JSON.stringify(tempQuestionFilters) ? 'btn-outline-primary' : 'btn-primary'" @click="updateQuestionFiltersAndQueryParams()">Mettre à jour les filtres !</button>
    </section>

  </section>
</template>

<script>
import FilterLabel from './FilterLabel.vue';
import DifficultyBadge from './DifficultyBadge.vue';

export default {
  name: 'QuestionFilter',
  props: {
    objectType: { type: String, default: 'question' },
    counter: { type: Number, default: 0 },
  },
  components: {
    FilterLabel,
    DifficultyBadge,
  },

  data() {
    return {
      tempQuestionFilters: {
        category: null,
        tag: null,
        author: null,
        difficulty: null,
      },
      showFilterBox: false,
    };
  },

  computed: {
    categories() {
      return this.$store.state.categories;
    },
    tags() {
      return this.$store.state.tags
        .slice(0) // .slice makes a copy of the array, instead of mutating the orginal
        .filter((t) => {
          return (this.objectType === 'question') ? t.question_count : t.quiz_count;
        })
        .sort((a, b) => a.name.localeCompare(b.name));
    },
    authors() {
      return this.$store.state.authors
        .slice(0) // .slice makes a copy of the array, instead of mutating the orginal
        .filter((a) => {
          return (this.objectType === 'question') ? a.question_count : a.quiz_count;
        })
        .sort((a, b) => {
          return (this.objectType === 'question') ? (b.question_count - a.question_count) : (b.quiz_count - a.quiz_count);
        });
    },
    difficultyLevels() {
      return this.$store.state.difficultyLevels;
    },
    questionFilters() {
      return this.$store.state.questionFilters;
    },
    questionsDisplayedCount() {
      return this.$store.state.questionsDisplayed.length;
    },
    quizzes() {
      return this.$store.state.quizzes;
    },
  },

  watch: {
    // eslint-disable-next-line
    objectType (newType, oldType) {
      this.updateQuestionFilters();
    },
    quizzes() {
      // We need to updateFilter because sometimes the quizzes
      // or questions doen't exist in mounted
      this.updateQuestionFilters();
    },
  },

  mounted() {
    if (Object.keys(this.$route.query).length) {
      Object.keys(this.$route.query).forEach((key) => {
        if (this.$route.query[key] !== null) {
          this.tempQuestionFilters[key] = this.$route.query[key];
        }
      });
    }
    this.updateQuestionFilters();
  },

  methods: {
    toggleFilterBox() {
      this.showFilterBox = !this.showFilterBox;
      this.tempQuestionFilters = { ...this.questionFilters };
    },
    updateTempQuestionFilter(data) {
      this.tempQuestionFilters[data.key] = (this.tempQuestionFilters[data.key] === data.value) ? null : data.value;
    },
    clearQuestionFilters() {
      this.$router.push({ query: {} });
      this.tempQuestionFilters = {
        category: null,
        tag: null,
        author: null,
        difficulty: null,
      };
      this.updateQuestionFilters();
    },
    updateQuestionFiltersAndQueryParams() {
      const query = {};
      Object.keys(this.tempQuestionFilters).forEach((key) => {
        if (this.tempQuestionFilters[key] !== null) {
          query[key] = this.tempQuestionFilters[key];
        }
      });
      this.$router.push({ query });
      this.updateQuestionFilters();
    },
    updateQuestionFilters() {
      this.showFilterBox = false;
      if (this.objectType === 'question') {
        this.$store.dispatch('UPDATE_QUESTION_FILTERS', this.tempQuestionFilters);
      } else {
        this.$store.dispatch('UPDATE_QUIZ_FILTERS', this.tempQuestionFilters);
      }
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
  cursor: pointer;
}
.filter-box > .filter-box--content {
  background-color: white;
  /* max-height: 65vh; */
  max-height: 50vh;
  overflow-y: scroll;
}
.filter-box > .filter-box--action {
  padding-top: 5px;
}
</style>
