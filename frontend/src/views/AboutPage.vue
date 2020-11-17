<template>
  <section class="text-align-left">
    <h2>A propos</h2>

    <section class="alert alert-primary" role="alert">
      Vous êtes un des premiers utilisateurs, merci d'être là !
      Ce site a été lancé en Mars 2020.
      Il est développé par quelques passionés, et a pour but d'évoluer en fonctions des retours utilisateurs :)
    </section>

    <h3>Pourquoi cette application ?</h3>
    <p>
      Le but est de rassembler un ensemble de connaissances - sur l'énérgie, le climat, et plus largement la crise climatique - sous forme de questions.
    </p>

    <p>
      Ces questions servent à sensibiliser (à édifier) sur la gravité de la situation et la diversité de ses facettes.
      Elles permettent (on l'espère) de déclencher la prise de conscience et amorcer le changement individuel.
    </p>

    <p>
      Ces questions peuvent aussi servir à se former pour mieux maitriser les chiffres et les ordres de grandeurs.
      Les usages peuvent être multiples (conférences, formations, quiz, jeu, etc.).
    </p>

    <br />
    <h3>Contribuer</h3>
    <p>
      On est preneur de tous vos retours !
    </p>
    <p>
      Une page <router-link :to="{ name: 'contribute' }">✍️&nbsp;Contribuer</router-link> vous permet de rajouter une question ou un sujet qui vous tiens à coeur.
      Vous pouvez aussi y laisser vos commentaires et remarques !
    </p>

    <br />
    <h3>Open source</h3>
    <p>
      Le code de l'application est visible sur <a href="https://github.com/raphodn/know-your-planet" target="_blank">la page Github de l'application</a>.
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
};
</script>
