<template>
  <section>
    <br />

    <h2>
      Tous les auteurs&nbsp;
      <span v-if="authors" class="text-secondary"><small>{{ authors.length }}</small></span>
    </h2>

    <br />

    <div v-if="loading" class="loading">
      Chargement des auteurs...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="authors && authors.length === 0">
      Pas d'auteurs :(
    </div>

    <div v-if="authors && authors.length > 0">
      <router-link class="no-decoration" v-for="author in authors" :key="author.author" :to="{ name: 'author-detail', params: { authorName: author.author } }">
        <span class="category">
          <h3>{{ author.author }}</h3>
          <p><strong>{{ author.question_count }}</strong> question<span v-if="author.question_count > 1">s</span></p>
        </span>
      </router-link>
    </div>

    <br />
    <hr v-if="authors" />
    <div v-if="authors" class="row actions">
      <div class="col-sm">
        <router-link :to="{ name: 'question-list' }">
          Toutes les questions
        </router-link>
        <br />
      </div>
      <div class="col-sm">
        <router-link :to="{ name: 'category-list' }">
          📂&nbsp;Toutes les catégories
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
  name: 'AuthorListPage',
  components: {
    HomeLink
  },

  data () {
    return {
      authors: null,
      loading: false,
      error: null,
    }
  },

  mounted () {
    this.fetchAuthors();
  },

  methods: {
    fetchAuthors() {
      this.error = this.authors = null;
      this.loading = true;
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/authors`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.authors = data;
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
  border: 1px solid #f3993f;
  border-radius: 5px;
  margin: 2.5px;
  padding: 5px;
  cursor: pointer;
}
</style>
