<template>
  <header>
    <div class="container-md">
      <nav class="navbar navbar-expand-lg navbar-light bg-light" role="navigation">
        <router-link class="navbar-brand" :to="{ name: 'home' }">
          <!-- <img src="/favicon-32x32.png" width="30" height="30" class="d-inline-block align-top" alt="Logo"> -->
          <img src="/logo_quiz_transparent.png" class="d-inline-block align-top" alt="Logo">
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
  font-weight: bold;
  letter-spacing: .05rem;
  /* background-color: #e9ecef; */
}
.navbar {
  padding: 0rem 1rem;
}
.navbar-brand img {
  max-width: 125px;
}
.navbar-collapse {
  justify-content: right;
}

@media (min-width: 992px) {
  .navbar {
    padding: 0rem 2rem;
  }
  .navbar-brand img {
    max-width: 175px;
  }
}
</style>
