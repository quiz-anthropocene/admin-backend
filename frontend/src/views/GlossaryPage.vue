<template>
  <section class="text-align-left">
    <h2>Glossaire</h2>

    <section class="alert alert-warning" role="alert" v-if="$i18n.locale === 'en'">
      🌐Page not yet translated ...
    </section>

    <p><i>Ces définitions sont ensuite affichées lorsque le mot apparait dans l'énoncé de la question.</i></p>

    <br />
    <hr />

    <section v-for="glossary_item in glossaire" :key="glossary_item.name">
      <h3>
        {{ glossary_item.name }}
        <small><i>{{ glossary_item.definition_short }}</i></small>
      </h3>
      <p>{{ glossary_item.description }}</p>
      <p class="glossary-link" v-if="glossary_item.description_accessible_url">
        🔗&nbsp;<a v-bind:href="glossary_item.description_accessible_url" target="_blank" v-bind:title="glossary_item.description_accessible_url">{{ glossary_item.description_accessible_url }}</a>
      </p>
      <p v-if="glossary_item.name_alternatives">
        <small>Similaire : {{ glossary_item.name_alternatives }}</small>
      </p>
      <hr />
    </section>

    <br />

    <section class="alert alert-warning" role="alert">
      Il manque un mot ? n'hésitez pas à nous le partager via le formulaire sur la page <router-link :to="{ name: 'contribute' }">Contribuer</router-link>.
    </section>

  </section>
</template>

<script>
import { metaTagsGenerator } from '../utils';

export default {
  name: 'GlossaryPage',
  metaInfo() {
    const title = 'Glossaire';
    return {
      meta: metaTagsGenerator(title),
    };
  },
  components: {
  },

  mounted() {
  },

  data() {
    return {
      // glossaire: null,
    };
  },

  computed: {
    glossaire() {
      return this.$store.state.ressources.glossaire;
    },
  },
};
</script>

<style scope>
p.glossary-link {
  white-space: nowrap;
  overflow-x: hidden;
  text-overflow: ellipsis;
}
</style>
