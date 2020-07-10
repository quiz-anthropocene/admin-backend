<template>
  <section class="text-align-left">
    <h2>Glossaire</h2>

    <hr />
    <section v-for="glossary_item in glossary" :key="glossary_item.name">
      <h3>
        {{ glossary_item.name }}
        <small><i>{{ glossary_item.definition_short }}</i></small>
      </h3>
      <p>{{ glossary_item.description }}</p>
      <p>🔗&nbsp;<a v-bind:href="glossary_item.description_accessible_url" target="_blank" v-bind:title="glossary_item.description_accessible_url">{{ glossary_item.description_accessible_url }}</a></p>
      <p v-if="glossary_item.name_alternatives"><small>Similaire : {{ glossary_item.name_alternatives }}</small></p>
      <hr />
    </section>

    <br />
    <section class="alert alert-warning" role="alert">
      Il manque un mot ? n'hésitez pas à nous le partager via le formulaire sur la page <router-link :to="{ name: 'contribute' }">Contribuer</router-link>.
    </section>

  </section>
</template>

<script>
export default {
  name: 'GlossaryPage',
  metaInfo: {
    title: 'Glossaire',
    meta: [
      { property: 'og:title', vmid: 'og:title', content: 'Glossaire' },
      { property: 'twitter:title', vmid: 'twitter:title', content: 'Glossaire' },
    ],
  },
  components: {
  },

  mounted() {
  },

  data() {
    return {
      // glossary: null,
    };
  },

  computed: {
    glossary() {
      return this.$store.state.glossary;
    },
  },
};
</script>
