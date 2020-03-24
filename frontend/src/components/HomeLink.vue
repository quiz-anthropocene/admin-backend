<template>
  <section>
    <br />
    <br />
    <div class="home small">
      <router-link :to="{ name: 'home' }">
        <!-- <button class="button">🏠&nbsp;Menu principal</button> -->
        Retour au menu principal
      </router-link>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HomeLink',
}
</script>

<style scoped>
</style>