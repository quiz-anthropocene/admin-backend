<template>
  <header>
    <h1 class="text-primary">
      <router-link class="no-decoration" :to="{ name: 'home' }">Know Your Planet</router-link>
    </h1>
    <h2 class="d-none d-sm-block" :class="{ 'd-block': currentRoute === 'home' }">
      Des questions/réponses pour mieux appréhender les limites de notre planète&nbsp;🌍
    </h2>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: {
  },

  computed: {
    currentRoute () {
      return this.$route.name;
    }
  }
}
</script>

<style scoped>
header {
  border: 10px solid var(--primary);
  margin: 10px;
  padding-left: 10px;
  padding-right: 10px;
}

@media(hover: hover) and (pointer: fine) {
  header h1 a:hover {
    text-shadow: 0px 0px 1px var(--primary);
  }
}
</style>
