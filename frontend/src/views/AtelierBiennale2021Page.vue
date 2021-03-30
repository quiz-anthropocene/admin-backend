<template>
  <section class="text-align-left">
    <h2>Atelier pour la Biennale des Villes en Transition <small>(1-4 avril 2021)</small></h2>

    <section v-if="$i18n.locale === 'en'" class="alert alert-warning" role="alert">
      🌐Page not yet translated ...
    </section>

    <p>
      Le quiz de l'anthropocène se décline désormais en atelier interactif !
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
      A l'occasion de la Biennale des Villes en Transition, proposée en ligne par la ville de Grenoble du 1er au 4 avril 2021,
      2 sessions vous sont proposées :
    </p>

    <ul>
      <li>Jeudi 1er avril, 16h à 19h</li>
      <li>Samedi 3 avril, 16h30 à 19h30</li>
    </ul>

    <p>
      <strong>Programme complet de la Biennale</strong> : <a href="https://www.grenoble.fr/628-biennale-des-villes-en-transition-2021-grenoble.htm" target="_blank">https://www.grenoble.fr/628-biennale-des-villes-en-transition-2021-grenoble.htm</a>
    </p>

    <p>
      <strong>Inscriptions</strong> : <a href="mailto:contact@quizanthropocene.fr">contact@quizanthropocene.fr</a> (préciser pour quelle session vous souhaitez vous inscrire).
    </p>

    <p>
      <strong>Jauge</strong> : 15 participants max par session.
    </p>

    <p>
      <strong><a href="https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/images/atelier/B21_affiche Quiz Anthropocène.pdf" target="_blank">Flyer (pdf, 1MB)</a></strong>
    </p>

    <img class="img-fluid" src="https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/images/atelier/biennale_villes_transition_2021.jpg" alt="Logo Biennale des Villes en Transition" />
  </section>
</template>

<script>
import { metaTagsGenerator } from '../utils';

export default {
  name: 'AboutPage',
  metaInfo() {
    const title = 'Atelier Biennale 2021';
    const description = 'Premier atelier intéractif, début avril 2021. Tous les détails ici.';
    const imageUrl = 'https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/images/atelier/biennale_villes_transition_2021.jpg';
    return {
      title,
      meta: metaTagsGenerator(title, description, imageUrl),
    };
  },
  components: {
  },

  computed: {
  },
};
</script>
