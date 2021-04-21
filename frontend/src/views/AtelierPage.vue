<template>
  <section class="text-align-left">
    <h2>Atelier Quiz de l’Anthropocène</h2>

    <section v-if="$i18n.locale === 'en'" class="alert alert-warning" role="alert">
      🌐Page not yet translated
    </section>

    <h4><i>Le quiz de l'anthropocène se décline désormais en atelier interactif !</i></h4>

    <p>
      Climat, biodiversité, épuisement des ressources, transformation des espaces, pandémies, montées des tensions…
      Nous sommes entrés dans l'anthropocène, une ère où l'humain est devenu la plus grande force qui façonne le monde.
    </p>

    <ul>
      <li>Comment développer sa lucidité vis à vis des dérèglements en cours ou à venir ?</li>
      <li>Où trouver des informations fiables sur l'état de notre monde et des projections sérieuses sur les futurs possibles ?</li>
      <li>Enfin, quels comportements et actions adopter pour préparer au mieux notre avenir et celui des générations suivantes ?</li>
    </ul>

    <p>
      C’est à ces questions vertigineuses que l’atelier Quiz de l’Anthropocène vous convie, de façon ludique, collective et pédagogique.
    </p>

    <p>
      A l'occasion de la Biennale des Villes en Transition, proposée en ligne par la ville de Grenoble en Avril 2021,
      nous avons pu valider le principe de cet atelier, qui a été apprécié par les participants !
    </p>

    <p>
      <strong>Jauge</strong> : 15 participants par session
    </p>
    <p>
      <strong>Durée</strong> : 2 heures
    </p>
    <p>
      <strong>Format</strong> : présentiel / distanciel, sous la houlette d’un animateur
    </p>

    <p>
      📅 <i>Prochaines dates à définir</i>
    </p>

    <p>
      Ca vous intéresse ? Pour en savoir plus, écrivez-nous à <a href="mailto:contact@quizanthropocene.fr">contact@quizanthropocene.fr</a>
    </p>
  </section>
</template>

<script>
import { metaTagsGenerator } from '../utils';

export default {
  name: 'AboutPage',
  metaInfo() {
    const title = 'Atelier';
    const description = "Le quiz de l'anthropocène se décline désormais en atelier interactif !";
    // const imageUrl = 'https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/images/atelier/biennale_villes_transition_2021.jpg';
    return {
      title,
      meta: metaTagsGenerator(title, description),
    };
  },
  components: {
  },

  computed: {
  },
};
</script>
