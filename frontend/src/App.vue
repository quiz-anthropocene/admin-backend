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

.button {
  margin: 1em 1em 0 1em;
  /* margin-left: 1em;
  margin-right: 1em; */
  /* margin: 1em; */
  padding: 0.5em 2em;
  font-size: 1em;
  /* text-decoration: none; */
  /* background-color: white; */
  /* border: 0; */
  cursor: pointer;
}

.color-blue {
  color: #005995;
}
.color-orange {
  color: #F33F3F;
}
</style>
