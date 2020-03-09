<template>
  <header>
    <h1 class="title">
      <router-link class="no-decoration" :to="{ name: 'home' }">Know Your Planet</router-link>
    </h1>
    <h2>Des questions/réponses pour mieux apréhender les limites de notre planète&nbsp;🌍</h2>
  </header>
</template>

<script>
export default {
  name: 'Header',
}
</script>

<style scoped>
  header {
    border: 10px solid #005995;
  }
  .title {
    color: #005995;
  }
  .title a:hover {
    text-shadow: 0px 0px 1px #005995;
  }
</style>