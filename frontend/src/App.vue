<template>
  <div id="app">
    <Header />
    <section>
      <div v-if="loading" class="alert alert-primary" role="alert">Chargement...</div>
      <div v-if="error" class="alert alert-danger" role="alert">
        Erreur de connexion 🤔
        <a href="#" @click="initData()">Réessayer</a>
      </div>
    </section>
    <main class="container-md">
      <router-view></router-view>
    </main>
    <br />
    <br />
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: {
    Header,
  },

  computed: {
    loading () {
      return this.$store.state.loading;
    },
    error () {
      return this.$store.state.error;
    }
  },

  mounted: function () {
    this.initData();
  },

  methods: {
    initData () {
      this.$store.dispatch('GET_QUESTION_LIST');
      this.$store.dispatch('GET_CATEGORY_LIST');
      this.$store.dispatch('GET_TAG_LIST');
    }
  }
}
</script>

<style lang="scss">

/* Override bootstrap.min.css */

$theme-colors: (
  "primary": #005995,
  "secondary": #F33F3F
);
$tag-color: #f3993f;

@import "../node_modules/bootstrap/scss/bootstrap";

html {
  background-color: #F8F8F8;
}
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #F8F8F8;
  text-align: center;
}

h1, h2, h3, h4, p {
  margin-top: 10px;
  margin-bottom: 10px;
}
h1 {
  font-size: 2em;
  font-weight: 700;
}
h2 {
  font-size: 1.5em;
  font-weight: 700;
}
h3 {
  font-size: 1.17em;
  font-weight: 700;
}

button {
  margin: 10px;
}


/* Global css */

a.no-decoration {
  color: inherit;
  text-decoration: inherit;
}

hr.custom-seperator {
  border: 0 none;
  height: 1px;
  width: 50%;
  color: var(--primary);
  background-color: var(--primary);
}

.row {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  margin: 0;
}
.row-item {
  flex: 0 1 100%;
  margin-bottom: 10px;
}

.margin-bottom-0 {
  margin-bottom: 0;
}
.margin-right-20 {
  margin-right: 20px;
}
.margin-top-bottom-10 {
  margin-top: 10px;
  margin-bottom: 10px;
}
.padding-top-bottom-15 {
  padding-top: 15px;
  padding-bottom: 15px;
}

.color-green {
  color: green;
}
.color-red {
  color: red;
}
.color-tag {
  color: $tag-color;
}

.text-underline-primary {
  text-decoration: underline;
  text-decoration-color: var(--primary);
}
.text-underline-secondary {
  text-decoration: underline;
  text-decoration-color: var(--secondary);
}
.text-underline-tag {
  text-decoration: underline;
  text-decoration-color: $tag-color;
}

.text-align-left {
  text-align: left;
}

.small {
  font-size: small;
}

.actions .col-sm {
  padding-bottom: 20px;
}


/* Elements */

.label {
  display: inline-block;
  border: 1px solid;
  border-radius: 5px;
  margin: 2.5px;
  padding: 5px;
  cursor: pointer;
}
.label-category {
  border-color: var(--secondary);
}
.label-category--active {
  background-color: #f88787;
  text-shadow: 0px 0px 1px black;
}
.label-tag {
  border-color: $tag-color;
}
.label-tag--active {
  background-color: #f8bf87;
  text-shadow: 0px 0px 1px black;
}


/* Media */

@media all and (min-width: 30em) {
  .row-item {
    max-width: calc(50% - 1em);
  }
}
@media all and (min-width: 60em) {
  .row-item {
    max-width: calc(33.33% - 1em);
  }
}

@media(hover: hover) and (pointer: fine) {
  .label-category:hover {
    background-color: #f88787;
  }
  .label-tag:hover {
    background-color: #f3993f;
  }
}
</style>
