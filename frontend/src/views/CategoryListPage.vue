<template>
  <section>
    <br />

    <h2>
      Toutes les catégories&nbsp;
      <span v-if="categories" class="text-secondary"><small>{{ categories.length }}</small></span>
    </h2>

    <br />

    <div v-if="loading" class="loading">
      Chargement des catégories...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="categories && categories.length === 0">
      Pas de catégories :(
    </div>

    <div v-if="categories && categories.length > 0">
      <router-link class="no-decoration" v-for="category in categories" :key="category.name" :to="{ name: 'category-detail', params: { categoryName: category.name } }">
        <span class="category">
          <h3>{{ category.name }}</h3>
          <p><strong>{{ category.question_count }}</strong> question<span v-if="category.question_count > 1">s</span></p>
        </span>
      </router-link>
    </div>

    <br />
    <hr v-if="categories" />
    <div v-if="categories" class="row actions">
      <div class="col-sm">
        <router-link :to="{ name: 'question-list' }">
          Toutes les questions
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
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'CategoryListPage',
  components: {
    HomeLink
  },

  data () {
    return {
      categories: null,
      loading: false,
      error: null,
    }
  },

  mounted () {
    this.fetchCategories();
  },

  methods: {
    fetchCategories() {
      this.error = this.categories = null;
      this.loading = true;
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/categories`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.categories = data;
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
.category {
  width: 300px;
  display: inline-block;
  border: 1px solid var(--secondary);
  border-radius: 5px;
  margin: 2.5px;
  padding: 5px;
  cursor: pointer;
}
</style>
