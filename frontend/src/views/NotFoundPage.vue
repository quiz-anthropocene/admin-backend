<template>
  <section>
    <h3>Page inconnue :(</h3>
  </section>
</template>

<script>
import { metaTagsGenerator } from '../utils';

export default {
  name: 'NotFoundPage',
  metaInfo() {
    const title = '404';
    return {
      meta: metaTagsGenerator(title),
    };
  },
  components: {
  },
};
</script>
