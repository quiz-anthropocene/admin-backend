<template>
  <div class="home">
    <router-link :to="{ name: 'home' }">
      🏠&nbsp;{{ $t('footer.home') }}
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'HomeLink',
};
</script>
