<template>
  <header>
    <div class="container-md">
      <nav class="navbar navbar-expand-lg navbar-light bg-light" role="navigation">
        <router-link class="navbar-brand" :to="{ name: 'home' }">
          <img src="/favicon-32x32.png" width="30" height="30" class="d-inline-block align-top" alt="Logo">
          Quiz de l'Anthropocène
        </router-link>
        <button class="navbar-toggler" @click="toggleNavbar" type="button" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div id="navbarNav" class="collapse navbar-collapse" :class="{ 'show': showNavbar }">
          <router-link class="nav-item nav-link" :to="{ name: 'quiz-list' }">{{ $t('messages.allQuizs') }}</router-link>
          <router-link class="nav-item nav-link" :to="{ name: 'contribute' }">{{ $t('footer.contribute') }}</router-link>
          <router-link class="nav-item nav-link" :to="{ name: 'about' }">{{ $t('footer.aboutShort') }}</router-link>
        </div>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: {
  },

  data() {
    return {
      showNavbar: false,
    };
  },

  computed: {
    currentRoute() {
      return this.$route.name;
    },
    configuration() {
      return this.$store.state.configuration;
    },
  },

  methods: {
    toggleNavbar() {
      this.showNavbar = !this.showNavbar;
    },
  },
};
</script>

<style scoped>
header {
  top: 0;
  position: sticky;
  z-index: 100;
  box-shadow: 0 2px 19px 0 rgb(56 56 56 / 10%);
  /* background-color: #e9ecef; */
}
.navbar-collapse {
  justify-content: right;
}
</style>
