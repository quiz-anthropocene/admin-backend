<template>
  <section class="text-align-left">
    <h2>A propos</h2>

    <section class="alert alert-primary" role="alert">
      Vous êtes un des premiers utilisateurs, merci d'être là !
      Ce site vient tout juste d'être lancé (Mars 2020), et a été développé par quelques passionés.
      Il a pour but d'évoluer en fonctions des retours utilisateurs :)
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
      Ces questions peuvent aussi servir à se former pour mieux maitriser les chiffres / ordres de grandeurs.
      Les usages peuvent être multiples (conférences, formations, quiz, jeu...).
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
      Si vous avez des commentaires ou des suggestions sur l'application, vous pouvez y créer des <i>Issues</i> 🙏
    </p>

    <br />
    <h3>Quelques chiffres</h3>
    <p>
      Voir la page <router-link :to="{ name: 'stats' }">📊&nbsp;Statistiques</router-link>.
    </p>

    <br />
    <h3>Nous connaître</h3>
    <p>
      Juste quelques <strong>bénévoles</strong> impliqués et concernés par les questions climat.
    </p>

    <br />
    <h3>Vous souhaitez aller plus loin ?</h3>
    <a href="https://fresqueduclimat.org/" target="_blank">La Fresque du Climat</a><br />
    <a href="https://theshiftproject.org/" target="_blank">The Shift Project</a><br />
    <a href="https://avenirclimatique.org/" target="_blank">Avenir Climatique</a><br />
    <a href="http://adrastia.org/" target="_blank">Adrastia</a><br />
    <a href="https://citoyenspourleclimat.org/" target="_blank">Citoyens pour le climat (CPLC)</a><br />
    <a href="https://extinctionrebellion.fr/" target="_blank">Extinction Rebellion (XR)</a><br />
    <a href="https://www.lpo.fr/" target="_blank">La Ligue pour la Protection des Oiseaux (LPO)</a><br />

    <h6>Mais aussi...</h6>
    <a href="https://www.hautconseilclimat.fr/" target="_blank">Le Haut conseil pour le climat</a><br />
    <a href="https://www.conventioncitoyennepourleclimat.fr/" target="_blank">La Convention Citoyenne pour le climat (CCC)</a><br />
  </section>
</template>

<script>
export default {
  name: 'AboutPage',
  metaInfo: {
    title: 'A Propos',
    meta: [
      { property: 'og:title', vmid: 'og:title', content: 'A Propos' },
      { property: 'twitter:title', vmid: 'twitter:title', content: 'A Propos' },
    ],
  },
  components: {
  },
};
</script>
