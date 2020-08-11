<template>
  <footer>
    <br />
    <section class="container-md">
      <div class="row">
        <!-- <div class="col-sm">
          <router-link :to="{ name: 'question-list' }">
            ❓&nbsp;Toutes les questions
          </router-link>
          <br />
        </div> -->
        <!-- Left link -->
        <div class="col-sm">
          <HomeLink />
        </div>
        <!-- Center link -->
        <div class="col-sm" v-if="currentRoute !== 'about'">
          <router-link :to="{ name: 'about' }">
            ℹ️&nbsp;À propos de cette application
          </router-link>
        </div>
        <div class="col-sm" v-if="currentRoute === 'about'">
          <!-- <router-link :to="{ name: 'glossary' }">
            📓&nbsp;Glossaire
          </router-link> -->
          <router-link :to="{ name: 'ressources' }">
            📚&nbsp;Ressources
          </router-link>
        </div>
        <!-- Right link -->
        <div class="col-sm" v-if="currentRoute !== 'quiz-detail'">
          <router-link :to="{ name: 'contribute' }">
            ✍️&nbsp;Contribuer
          </router-link>
        </div>
        <div class="col-sm" v-if="currentRoute === 'quiz-detail'">
          <router-link :to="{ name: 'quiz-list' }">
            🕹&nbsp;Tous les quiz
          </router-link>
          <br />
        </div>
      </div>
    </section>
  </footer>
</template>

<script>
import HomeLink from './HomeLink.vue';

export default {
  name: 'Footer',
  components: {
    HomeLink,
  },
  props: {
  },

  computed: {
    currentRoute() {
      return this.$route.name;
    },
  },
};
</script>

<style scoped>
footer {
  margin-top: 40px;
  background-color: #e9ecef;
}

.row > .col-sm {
  padding-bottom: 20px;
}
</style>
