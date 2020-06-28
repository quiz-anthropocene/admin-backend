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
// import GlossaryYamlData from '../data/glossary.yaml';

export default {
  name: 'GlossaryPage',
  metaInfo: {
    title: 'Glossaire',
  },
  components: {
  },

  mounted() {
    // this.$store.dispatch('GET_GLOSSARY_LIST_FROM_LOCAL_YAML');
  },

  data() {
    return {
      // glossary: GlossaryYamlData
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
