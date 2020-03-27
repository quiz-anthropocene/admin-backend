<template>
  <section>
    <br />

    <h2>
      <router-link class="no-decoration" :to="{ name: 'category-list' }">Catégorie:</router-link>&nbsp;
      <span class="text-secondary">{{ currentCategory }}</span>
    </h2>

    <br />

    <div v-if="loading" class="loading">
      Chargement des questions...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="questions && questions.length === 0">
      Pas de questions dans cette catégorie :(
    </div>

    <!-- Question List -->
    <div v-if="questions && questions.length > 0" class="row">
      <div class="row-item row-item-question" v-for="question in questions" :key="question.id">
        <router-link class="no-decoration" :to="{ name: 'question-detail', params: { questionId: question.id } }">
          <QuestionCard v-bind:question="question" />
        </router-link>
      </div>
    </div>

    <br />
    <br />
    <div v-if="questions" class="row">
      <div class="col-sm">
        <router-link :to="{ name: 'contribute'  }">
          ✍️&nbsp;Ajouter une question <span class="text-secondary">{{ currentCategory }}</span>
        </router-link>
      </div>
      <div class="col-sm">
        <router-link :to="{ name: 'category-list'  }">
          🏷️&nbsp;Toutes les catégories
        </router-link>
      </div>
      <div class="col-sm">
        <HomeLink />
      </div>
    </div>
  </section>
</template>

<script>
import QuestionCard from './QuestionCard.vue'
import HomeLink from './HomeLink.vue'

export default {
  name: 'CategoryDetailPage',
  components: {
    QuestionCard,
    HomeLink
  },

  data () {
    return {
      currentCategory: null,
      questions: null,
      loading: false,
      error: null,
    }
  },

  mounted () {
    this.currentCategory = this.$route.params.categoryKey;
    this.fetchCategoryQuestions(this.$route.params.categoryKey);
  },

  methods: {
    fetchCategoryQuestions(currentCategoryKey) {
      const params = { 'category': currentCategoryKey };
      const urlParams = new URLSearchParams(Object.entries(params));
      this.error = this.questions = null;
      this.loading = true;
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions?${urlParams}`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.questions = data;
        })
        .catch(error => {
          console.log(error)
          this.error = error;
        })
    },
  }
}
</script>

<style scoped>
.row-item-question {
  height: 150px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.1s;
  border: 2px solid #005995;
  border-radius: 5px;
  cursor: pointer;
}

@media(hover: hover) and (pointer: fine) {
  .category:hover {
    background-color: #f88787;
  }
  .row-item-question:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
}
</style>