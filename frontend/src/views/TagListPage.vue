<template>
  <section>
    <br />

    <h2>
      Tous les tags&nbsp;
      <span v-if="tags" class="text-secondary"><small>{{ tags.length }}</small></span>
    </h2>

    <br />

    <div v-if="tags && tags.length === 0">
      Pas de tags :(
    </div>

    <div v-if="tags && tags.length > 0">
      <router-link class="no-decoration" v-for="tag in tags" :key="tag.name" :to="{ name: 'tag-detail', params: { tagName: tag.name } }">
        <span class="category">
          <h3>{{ tag.name }}</h3>
          <p><strong>{{ tag.question_count }}</strong> question<span v-if="tag.question_count > 1">s</span></p>
        </span>
      </router-link>
    </div>
  </section>
</template>

<script>
export default {
  name: 'TagListPage',
  metaInfo: {
    title: 'Tags',
  },
  components: {
  },

  data() {
    return {
      // tags: null,
    };
  },

  computed: {
    tags() {
      return this.$store.state.tags;
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
  border: 1px solid #f3993f;
  border-radius: 5px;
  margin: 2.5px;
  padding: 5px;
  cursor: pointer;
}
</style>
