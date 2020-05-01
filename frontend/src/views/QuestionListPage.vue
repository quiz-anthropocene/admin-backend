<template>
  <section>
    <br />
    
    <!-- Filtre: catégorie -->
    <div v-if="categories">
      <span v-for="category in categories" :key="category.name" class="label label-category" :class="{ 'label-category--active' : category.name === categorySelected }" @click="clickCategory(category.name)">
        {{ category.name }} <small><i>{{ category.question_count }}</i></small>
      </span>
    </div>

    <br />
    
    <!-- Filtre: tag -->
    <div v-if="tags">
      <span v-for="tag in tags" :key="tag.name" class="label label-tag" :class="{ 'label-tag--active' : tag.name === tagSelected }" @click="clickTag(tag.name)">
        {{ tag.name }} <small><i>{{ tag.question_count }}</i></small>
      </span>
    </div>

    <br />

    <!-- Filtre: author -->
    <div v-if="authors">
      <span v-for="author in authors" :key="author.name" class="label label-author" :class="{ 'label-author--active' : author.name === authorSelected }" @click="clickAuthor(author.name)">
        {{ author.name }} <small><i>{{ author.question_count }}</i></small>
      </span>
    </div>

    <br />

    <!-- Filtre: difficulty -->
    <div v-if="difficultyLevels">
      <span v-for="difficulty in difficultyLevels" :key="difficulty.name" class="label label-difficulty" :class="{ 'label-difficulty--active' : difficulty.value === difficultySelected }" @click="clickDifficulty(difficulty.value)">
        <small><DifficultyBadge v-bind:difficulty="difficulty.value" /></small> <small><i>{{ difficulty.question_count }}</i></small>
      </span>
    </div>

    <br />

    <!-- Question List -->
    <div v-if="questions" class="row">
      <div class="row-item row-item-question" v-for="question in questionsDisplayed" :key="question.id">
        <router-link class="no-decoration" :to="{ name: 'question-detail', params: { questionId: question.id } }">
          <QuestionPreviewCard v-bind:question="question" />
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
import QuestionPreviewCard from '../components/QuestionPreviewCard.vue'
import DifficultyBadge from '../components/DifficultyBadge.vue'
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'QuestionListPage',
  components: {
    QuestionPreviewCard,
    DifficultyBadge,
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
      // authors: null
      authorSelected: null,
      // difficultyLevels: null
      difficultySelected: null,
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
    },
    authors () {
      return this.$store.state.authors;
    },
    difficultyLevels () {
      return this.$store.state.difficultyLevels;
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
    clickAuthor(author) {
      this.authorSelected = (this.authorSelected === author) ? null : author;
      this.updateQuestionsDisplayed();
    },
    clickDifficulty(difficulty) {
      this.difficultySelected = (this.difficultySelected === difficulty) ? null : difficulty;
      this.updateQuestionsDisplayed();
    },
    updateQuestionsDisplayed() {
      this.questionsDisplayed = this.$store.getters.getQuestionsByFilter({
        "categoryName": this.categorySelected,
        "tagName": this.tagSelected,
        "authorName": this.authorSelected,
        "difficulty": this.difficultySelected
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
  .row-item-question:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
}
</style>
