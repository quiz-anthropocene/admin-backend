<template>
  <section>
    <br />

    <div>
      <router-link class="no-decoration" v-for="category in categories" :key="category.key" :to="{ name: 'category-detail', params: { categoryKey: category.key } }">
        <span class="category">
          {{ category.name }}<br />
          <small><strong>{{ category.question_count }}</strong> question<span v-if="category.question_count > 1">s</span></small>
        </span>
      </router-link>
    </div>
  </section>
</template>

<script>
export default {
  name: 'CategoryListPage',

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
  display: inline-block;
  border: 1px solid #F33F3F;
  border-radius: 5px;
  margin: 2.5px;
  padding: 5px;
  cursor: pointer;
}
.category-active {
  background-color: #f88787;
  text-shadow: 0px 0px 1px black;
}
</style>