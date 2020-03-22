<template>
  <div id="app">
    <Header />
    <main>
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

<style>
html {
  background-color: #F8F8F8;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin-top: 8px;
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
}

h1, h2, h3, h4, p {
    margin-top: 10px;
    margin-bottom: 10px;
  }

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
}
.row-item {
  flex: 0 1 100%;
  margin-bottom: 10px;
}

.button {
  margin: 1em 1em 0 1em;
  padding: 0.5em 2em;
  font-size: 1em;
  cursor: pointer;
}

.small-container {
  max-width: 600px;
  margin: 0 auto;
}

.margin-bottom-0 {
  margin-bottom: 0;
}
.margin-right-20 {
  margin-right: 20px;
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

@media all and (max-width: 40em) {
  .hidden-sm {
    display: none;
  }
}
@media all and (min-width: 40em) {
  .row-item {
    max-width: calc(50% - 1em);
  }
  .visible-sm {
    display: none;
  }
}
@media all and (min-width: 60em) {
  .row-item {
    max-width: calc(33.33% - 1em);
  }
}
</style>
