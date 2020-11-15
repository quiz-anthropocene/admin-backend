<template>
  <header>
    <div>
      <h1 class="text-primary">
        <router-link class="no-decoration" :to="{ name: 'home' }">Quiz de l'Anthropocène</router-link>
      </h1>
      <h2 class="d-none d-sm-block" :class="{ 'd-block': currentRoute === 'home' }">
        Des questions/réponses pour mieux appréhender les limites de notre planète&nbsp;🌍
      </h2>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: {
  },

  computed: {
    currentRoute() {
      return this.$route.name;
    },
  },
};
</script>

<style scoped>
header {
  background-image: url("https://showyourstripes.info/stripes/GLOBE---1850-2019-MO.png");
  background-size: cover;
  border-radius: 5px;
  margin: 10px;
  padding: 15px;
}

header > div {
  background-color: white;
  padding: 5px;
}

@media(hover: hover) and (pointer: fine) {
  header h1 a:hover {
    text-shadow: 0px 0px 1px var(--primary);
  }
}
</style>
