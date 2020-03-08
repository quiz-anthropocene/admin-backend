<template>
  <div id="app">
    <Header />
    <main>
      <router-view></router-view>
    </main>
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

a.no-decoration {
  color: inherit;
  text-decoration: inherit;
}
</style>
