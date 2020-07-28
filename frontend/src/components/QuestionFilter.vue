<template>
  <section class="filter-box">

    <!-- Header -->
    <div class="filter-box--header" :class="{ 'padding-bottom-10': showFilterBox }" @click="toggleFilterBox()">
      <div class="row no-gutters">
        <div class="col-sm-8">
          <span class="label label-hidden">
            <span>⚙️&nbsp;Filtres&nbsp;</span>
            <span v-if="!showFilterBox">▸</span> <!-- ▲ ► -->
            <span v-if="showFilterBox">▾</span> <!-- ▼ -->
          </span>
          <span v-for="(value, key) in questionFilters" :key="key">
            <span v-if="(key === 'category') && value" class="label label-category">{{ value }}</span>
            <span v-if="(key === 'tag') && value" class="label label-tag">{{ value }}</span>
            <span v-if="(key === 'author') && value" class="label label-author">{{ value }}</span>
            <span v-if="(key === 'difficulty') && (value !== null)" class="label label-difficulty"><DifficultyBadge v-bind:difficulty="value" /></span>
          </span>
        </div>
        <div class="col-sm-4 text-align-right">
          <span class="label label-hidden"><strong>{{ questionsDisplayedCount }}</strong> Questions</span>
        </div>
      </div>
    </div>

    <!-- Content -->
    <section v-if="showFilterBox" class="filter-box--content">

      <!-- <hr class="custom-separator" /> -->

      <div v-if="categories">
        <h3>📂&nbsp;Catégories</h3>
        <FilterLabel v-for="category in categories" :key="category.name" @filterLabelClicked="updateTempQuestionFilter"
          filterType="category" v-bind:filterObject="category" v-bind:customClass="(category.name === tempQuestionFilters['category']) ? 'label-category--active' : ''" />
      </div>

      <hr class="custom-separator" />

      <div v-if="tags">
        <h3>🏷️&nbsp;Tags</h3>
        <FilterLabel v-for="tag in tags" :key="tag.name" @filterLabelClicked="updateTempQuestionFilter"
          filterType="tag" v-bind:filterObject="tag" v-bind:customClass="(tag.name === tempQuestionFilters['tag']) ? 'label-tag--active' : ''" />
      </div>

      <hr class="custom-separator" />

      <div v-if="authors">
        <h3>📝&nbsp;Auteurs</h3>
        <FilterLabel v-for="author in authors" :key="author.name" @filterLabelClicked="updateTempQuestionFilter"
          filterType="author" v-bind:filterObject="author" v-bind:customClass="(author.name === tempQuestionFilters['author']) ? 'label-author--active' : ''" />
      </div>

      <hr class="custom-separator" />

      <div v-if="difficultyLevels">
        <h3>🏆&nbsp;Difficultés</h3>
        <FilterLabel v-for="difficulty in difficultyLevels" :key="difficulty.name" @filterLabelClicked="updateTempQuestionFilter"
          filterType="difficulty" v-bind:filterObject="difficulty" v-bind:customClass="(difficulty.value === tempQuestionFilters['difficulty']) ? 'label-difficulty--active' : ''" />
      </div>

      <br />
    </section>

    <!-- Action Buttons -->
    <section v-if="showFilterBox" class="filter-box--action">
      <button class="btn btn-outline-secondary margin-5" @click="clearQuestionFilters()">Réinitialiser</button>
      <button class="btn btn-outline-dark margin-5" @click="toggleFilterBox()">Annuler</button>
      <button class="btn margin-5" :class="JSON.stringify(questionFilters) === JSON.stringify(tempQuestionFilters) ? 'btn-outline-primary' : 'btn-primary'" @click="updateQuestionFilters()">Mettre à jour les filtres !</button>
    </section>

  </section>
</template>

<script>
import FilterLabel from './FilterLabel.vue';
import DifficultyBadge from './DifficultyBadge.vue';

export default {
  name: 'QuestionFilter',
  props: {
  },
  components: {
    FilterLabel,
    DifficultyBadge,
  },

  data() {
    return {
      tempQuestionFilters: {},
      showFilterBox: false,
    };
  },

  computed: {
    categories() {
      return this.$store.state.categories;
    },
    tags() {
      // .slice makes a copy of the array, instead of mutating the orginal
      return this.$store.state.tags.slice(0).filter((t) => t.question_count);
    },
    authors() {
      // .slice makes a copy of the array, instead of mutating the orginal
      return this.$store.state.authors.slice(0).sort((a, b) => b.question_count - a.question_count);
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
  },

  methods: {
    toggleFilterBox() {
      this.showFilterBox = !this.showFilterBox;
      this.tempQuestionFilters = { ...this.questionFilters };
    },
    updateTempQuestionFilter(data) {
      console.log(data, this.tempQuestionFilters);
      this.tempQuestionFilters[data.key] = (this.tempQuestionFilters[data.key] === data.value) ? null : data.value;
    },
    clearQuestionFilters() {
      this.showFilterBox = !this.showFilterBox;
      this.tempQuestionFilters = {
        category: null,
        tag: null,
        author: null,
        difficulty: null,
      };
      this.$store.dispatch('UPDATE_QUESTION_FILTERS', this.tempQuestionFilters);
    },
    updateQuestionFilters() {
      this.showFilterBox = !this.showFilterBox;
      this.$store.dispatch('UPDATE_QUESTION_FILTERS', this.tempQuestionFilters);
    },
  },
};
</script>

<style scoped>
.filter-box {
  box-shadow: 0px 0px 5px 5px #dfdfdf;
  border-radius: 5px;
  margin: 10px 0px;
  padding: 10px;
  max-height: 80vh;
  overflow: auto;
}
.filter-box > .filter-box--header {
  text-align: left;
  cursor: pointer;
}
.filter-box > .filter-box--content {
  background-color: white;
  max-height: 50vh;
  overflow-y: scroll;
}
.filter-box > .filter-box--action {
  padding-top: 10px;
}
</style>
