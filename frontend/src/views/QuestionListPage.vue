<template>
  <section>
    <br />
    
    <!-- Filtre: catégorie -->
    <div v-if="categories">
      <span v-for="category in categories" :key="category.name" class="label label-category" :class="{ 'label-category--active' : category.name === categorySelected }" @click="clickCategory(category.name)">
        {{ category.name }}
      </span>
    </div>

    <br />
    
    <!-- Filtre: tag -->
    <div v-if="tags">
      <span v-for="tag in tags" :key="tag.name" class="label label-tag" :class="{ 'label-tag--active' : tag.name === tagSelected }" @click="clickTag(tag.name)">
        {{ tag.name }}
      </span>
    </div>

    <br />

    <div v-if="loading" class="loading">
      Chargement des questions...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <!-- Question List -->
    <div v-if="questions" class="row">
      <div class="row-item row-item-question" v-for="question in questionsDisplayed" :key="question.id">
        <router-link class="no-decoration" :to="{ name: 'question-detail', params: { questionId: question.id } }">
          <QuestionCard v-bind:question="question" />
        </router-link>
      </div>
    </div>

    <br />
    <hr v-if="questions" />
    <div v-if="questions" class="row actions">
      <div class="col-sm">
        <router-link :to="{ name: 'category-list' }">
          📂&nbsp;Toutes les catégories
        </router-link>
        <br />
      </div>
      <div class="col-sm">
        <router-link :to="{ name: 'tag-list' }">
          🏷️&nbsp;Tous les tags
        </router-link>
        <br />
      </div>
      <div class="col-sm">
        <HomeLink />
      </div>
    </div>
  </section>
</template>

<script>
import QuestionCard from '../components/QuestionCard.vue'
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'QuestionListPage',
  components: {
    QuestionCard,
    HomeLink
  },

  data () {
    return {
      // questions: null,
      questionsDisplayed: null,
      // categories: null,
      categorySelected: null,
      // tags: null,
      tagSelected: null,
      loading: false,
      error: null,
    }
  },

  computed: {
    questions () {
      return this.$store.state.questions;
    },
    categories () {
      return this.$store.state.categories;
    },
    tags () {
      return this.$store.state.tags;
    }
  },

  watch: {
    // eslint-disable-next-line
    questions (newQuestions, oldQuestions) {
      this.questionsDisplayed = newQuestions;
    }
  },

  mounted () {
    this.questionsDisplayed = this.questions;
  },

  methods: {
    clickCategory(category) {
      this.categorySelected = (this.categorySelected === category) ? null : category;
      this.updateQuestionsDisplayed();
    },
    clickTag(tag) {
      this.tagSelected = (this.tagSelected === tag) ? null : tag;
      this.updateQuestionsDisplayed();
    },
    updateQuestionsDisplayed() {
      this.questionsDisplayed = this.$store.getters.getQuestionsByFilter({
        "categoryName": this.categorySelected,
        "tagName": this.tagSelected
      });
    }
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
  .label-category:hover {
    background-color: #f88787;
  }
  .row-item-question:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
}
</style>
