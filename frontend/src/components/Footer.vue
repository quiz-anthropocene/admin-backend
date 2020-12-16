<template>
  <footer>
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
      <div class="row">
        <div class="col-sm">
          <a class="no-after" :href="configuration.application_linkedin_url" target="_blank"><img height="30px" src="openmoji_linkedin_E046.svg" alt="Linkedin" title="Linkedin" /></a>
          <a class="no-after" :href="configuration.application_twitter_url" target="_blank"><img height="30px" src="openmoji_twitter_E040.svg" alt="Twitter" title="Twitter" /></a>
          <a class="no-after" :href="configuration.application_facebook_url" target="_blank"><img height="30px" src="openmoji_facebook_E042.svg" alt="Facebook" title="Facebook" /></a>
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
    configuration() {
      return this.$store.state.configuration;
    },
  },
};
</script>

<style scoped>
footer {
  margin-top: 40px;
  background-color: #e9ecef;
  padding: 10px;
}

.row > .col,
.row > .col-sm {
  padding-top: 5px;
  padding-bottom: 5px;
}

.row > .col-sm > a > img {
  margin-left: 10px;
  margin-right: 10px;
}
</style>
