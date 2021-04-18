<template>
  <section class="text-align-left">
    <h2>A propos</h2>

    <!-- <section class="alert alert-primary" role="alert">
      Vous êtes un des premiers utilisateurs, merci d'être là !
      Ce site a été lancé en Mars 2020.
      Il est développé par quelques passionés, et a pour but d'évoluer en fonctions des retours utilisateurs :)
    </section> -->

    <section v-if="$i18n.locale === 'en'" class="alert alert-warning" role="alert">
      🌐Page not yet translated
    </section>

    <h3>Pourquoi cette application ?</h3>
    <div v-html="configuration.application_about"></div>

    <br />
    <h3>Contribuer</h3>
    <p>
      On est preneur de tous vos retours !
    </p>
    <p>
      Une page <router-link :to="{ name: 'contribute' }">✍️&nbsp;Contribuer</router-link>
      vous permet de rajouter une question ou un sujet qui vous tiens à coeur.
      Vous pouvez aussi y laisser vos commentaires et remarques !
    </p>

    <br />
    <h3>Open source</h3>
    <p>
      Le code de l'application est visible sur
      <a v-bind:href="configuration.application_open_source_code_url" target="_blank" title="Lien vers le code de l'application">la page Github de l'application</a>.
      Si vous avez des commentaires ou des suggestions sur l'application, vous pouvez y créer des <i>Issues</i>.
    </p>

    <br />
    <h3>Quelques chiffres</h3>
    <p>
      La page <router-link :to="{ name: 'stats' }">📊&nbsp;Statistiques</router-link> présente quelques chiffres d'usage.
    </p>

    <br />
    <h3>Nous connaître</h3>
    <p>
      Juste quelques <strong>bénévoles</strong> impliqués et concernés par les questions climat.
    </p>
    <p>
      Vous pouvez nous contacter à l'adresse <strong>contact [at] quizanthropocene.fr</strong>
    </p>

    <br />
    <h3>Vous souhaitez aller plus loin ?</h3>
    <p>
      On a créé une page <router-link :to="{ name: 'ressources' }">📚&nbsp;Ressources</router-link> pour regrouper
      plein d'informations additionnelles : des assos, d'autres projets similaires, nos lectures pour trouver les questions, etc.
    </p>

  </section>
</template>

<script>
import { metaTagsGenerator } from '../utils';

export default {
  name: 'AboutPage',
  metaInfo() {
    const title = 'A Propos';
    const description = 'Des informations sur cette application';
    return {
      title,
      meta: metaTagsGenerator(title, description),
    };
  },
  components: {
  },

  computed: {
    configuration() {
      return this.$store.state.configuration;
    },
  },
};
</script>
