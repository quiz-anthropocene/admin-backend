<template>
  <div id="app">
    <Header />
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
  }
}
</script>

<style lang="scss">

/* Override bootstrap.min.css */

$theme-colors: (
  "primary": #005995,
  "secondary": #F33F3F
);

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
  color: #005995;
  background-color: #005995;
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

/* .button {
  margin: 1em 1em 0 1em;
  padding: 0.5em 1em;
  font-size: 1em;
  cursor: pointer;
} */

// .small-container {
//   max-width: 600px;
//   margin: 0 auto;
// }

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

.color-blue {
  color: #005995;
}
.color-orange {
  color: #F33F3F;
}
.color-red {
  color: red;
}

.text-align-left {
  text-align: left;
}

.small {
  font-size: small;
}

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
</style>
