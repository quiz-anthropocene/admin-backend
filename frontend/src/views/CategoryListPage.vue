<template>
  <section>
    <br />

    <h2>
      Toutes les catégories&nbsp;
      <span v-if="categories" class="text-secondary"><small>{{ categories.length }}</small></span>
    </h2>

    <br />

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
  </section>
</template>

<script>
export default {
  name: 'CategoryListPage',
  metaInfo: {
    title: 'Catégories',
  },
  components: {
  },

  data() {
    return {
      // categories: null,
    };
  },

  computed: {
    categories() {
      return this.$store.state.categories;
    },
  },

  mounted() {
  },

  methods: {
  },
};
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
