<template>
  <section class="filter-box">
    <div class="filter-box--header text-align-left" @click="toggleFilterBox()">
      <span class="label-hidden">
        <span>⚙️&nbsp;Filtres&nbsp;</span>
        <span v-if="!showFilterBox">▲</span> <!-- ► -->
        <span v-if="showFilterBox">▼</span>
      </span>
      <span v-for="(value, key) in questionFilters" :key="key">
        <span v-if="(key === 'category') && value" class="label label-category">{{ value }}</span>
        <span v-if="(key === 'tag') && value" class="label label-tag">{{ value }}</span>
        <span v-if="(key === 'author') && value" class="label label-author">{{ value }}</span>
        <span v-if="(key === 'difficulty') && value" class="label label-difficulty">{{ value }}</span>
      </span>
      <span class="label-hidden" style="float:right"><strong>{{ questionsDisplayedCount }}</strong> Questions</span>
    </div>
    <section v-if="showFilterBox" class="filter-box--content">

      <hr class="custom-seperator" />

      <div v-if="categories">
        <h3>Catégories</h3>
        <span v-for="category in categories" :key="category.name" class="label label-category" :class="{ 'label-category--active' : category.name === tempQuestionFilters['category'] }" @click="updateTempQuestionFilter('category', category.name)">
          {{ category.name }} <small><i>{{ category.question_count }}</i></small>
        </span>
      </div>

      <hr class="custom-seperator" />

      <div v-if="tags">
        <h3>Tags</h3>
        <span v-for="tag in tags" :key="tag.name" class="label label-tag" :class="{ 'label-tag--active' : tag.name === tempQuestionFilters['tag'] }" @click="updateTempQuestionFilter('tag', tag.name)">
          {{ tag.name }} <small><i>{{ tag.question_count }}</i></small>
        </span>
      </div>

      <hr class="custom-seperator" />

      <div v-if="authors">
        <h3>Auteurs</h3>
        <span v-for="author in authors" :key="author.name" class="label label-author" :class="{ 'label-author--active' : author.name === tempQuestionFilters['author'] }" @click="updateTempQuestionFilter('author', author.name)">
          {{ author.name }} <small><i>{{ author.question_count }}</i></small>
        </span>
      </div>

      <hr class="custom-seperator" />

      <div v-if="difficultyLevels">
        <h3>Difficultés</h3>
        <span v-for="difficulty in difficultyLevels" :key="difficulty.name" class="label label-difficulty" :class="{ 'label-difficulty--active' : difficulty.value === tempQuestionFilters['difficulty'] }" @click="updateTempQuestionFilter('difficulty', difficulty.value)">
          <small><DifficultyBadge v-bind:difficulty="difficulty.value" /></small> <small><i>{{ difficulty.question_count }}</i></small>
        </span>
      </div>

      <hr class="custom-seperator" />

      <button class="btn btn-outline-secondary" @click="clearQuestionFilters()">Réinitialiser</button>
      <button class="btn btn-outline-secondary" @click="toggleFilterBox()">Annuler</button>
      <button class="btn" :class="JSON.stringify(questionFilters) === JSON.stringify(tempQuestionFilters) ? 'btn-outline-primary' : 'btn-primary'" @click="updateQuestionFilters()">Mettre à jour les filtres !</button>
    </section>

  </section>
</template>

<script>
import DifficultyBadge from '../components/DifficultyBadge.vue'

export default {
  name: 'QuestionFilter',
  props: {
  },
  components: {
    DifficultyBadge
  },

  data () {
    return {
      tempQuestionFilters: {},
      showFilterBox: false,
    }
  },

  computed: {
    categories () {
      return this.$store.state.categories;
    },
    tags () {
      return this.$store.state.tags;
    },
    authors () {
      return this.$store.state.authors;
    },
    difficultyLevels () {
      return this.$store.state.difficultyLevels;
    },
    questionFilters () {
      return this.$store.state.questionFilters;
    },
    questionsDisplayedCount () {
      return this.$store.state.questionsDisplayed.length;
    }
  },

  methods: {
    toggleFilterBox() {
      this.showFilterBox = !this.showFilterBox;
      this.tempQuestionFilters = {...this.questionFilters};
    },
    updateTempQuestionFilter(key, value) {
      this.tempQuestionFilters[key] = (this.tempQuestionFilters[key] === value) ? null : value;
    },
    clearQuestionFilters() {
      this.showFilterBox = !this.showFilterBox;
      this.tempQuestionFilters = {
        "category": null,
        "tag": null,
        "author": null,
        "difficulty": null,
      }
      this.$store.dispatch('UPDATE_QUESTION_FILTERS', this.tempQuestionFilters);
    },
    updateQuestionFilters() {
      this.showFilterBox = !this.showFilterBox;
      this.$store.dispatch('UPDATE_QUESTION_FILTERS', this.tempQuestionFilters);
    }
  }
}
</script>

<style scoped>
.filter-box {
  /* border: 1px solid var(--primary); */
  box-shadow: 0px 0px 5px 5px #dfdfdf;
  border-radius: 5px;
  margin: 10px 0px;
  padding: 10px;
}
.filter-box--header {
  cursor: pointer;
}
.filter-box--content {
  max-height: 500px;
  overflow-y: scroll;
}
</style>
