<template>
  <section class="text-align-left">
    <h2>Licence</h2>

    <h3>Utilisation non-commerciale</h3>
    <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">
      <img src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Licence Creative Commons" style="border-width:0" />
    </a>
    <p>
      Cette œuvre est mise à disposition selon les termes de la licence <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">Creative Commons BY-NC-SA 4.0</a>.
      <ul>
        <li>BY : Attribution</li>
        <li>NC : Pas d'utilisation commerciale</li>
        <li>SA : Partage dans les mêmes conditions</li>
      </ul>
    </p>

    <br />
    <h3>Utilisation commerciale</h3>
    <p>
      Vous pouvez nous contacter à l'adresse <strong>contact [at] quizanthropocene.fr</strong> pour en discuter.
    </p>

    <br />
  </section>
</template>

<script>
import { metaTagsGenerator } from '../utils';

export default {
  name: 'LicensePage',
  metaInfo() {
    const title = 'Licence';
    const description = 'Utilisation et réutilisation du contenu de l\'application';
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
