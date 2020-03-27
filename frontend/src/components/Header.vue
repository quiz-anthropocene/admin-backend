<template>
  <header>
    <h1 class="title">
      <router-link class="no-decoration" :to="{ name: 'home' }">Know Your Planet</router-link>
    </h1>
    <h2>Des questions/réponses pour mieux appréhender les limites de notre planète&nbsp;🌍</h2><!-- class="d-none d-sm-block" -->
  </header>
</template>

<script>
export default {
  name: 'Header',

  mounted () {
    console.log(this.$route);
  },

  beforeRouteUpdate (to, from, next) {
    console.log(to, from)
    next();
  },
}
</script>

<style scoped>
header {
  border: 10px solid #005995;
  margin: 10px;
  padding-left: 10px;
  padding-right: 10px;
}
.title {
  color: #005995;
}

@media(hover: hover) and (pointer: fine) {
  .title a:hover {
    text-shadow: 0px 0px 1px #005995;
  }
}
</style>