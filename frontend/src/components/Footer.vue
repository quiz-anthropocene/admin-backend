<template>
  <footer>
    <section class="container-md">
      <div class="row">
        <!-- <div class="col-sm">
          <router-link :to="{ name: 'question-list' }">
            ❓&nbsp;{{ $t('footer.allQuestions') }}
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
            ℹ️&nbsp;{{ $t('footer.about') }}
          </router-link>
        </div>
        <div class="col-sm" v-if="currentRoute === 'about'">
          <!-- <router-link :to="{ name: 'glossary' }">
            📓&nbsp;{{ $t('footer.glossary') }}
          </router-link> -->
          <router-link :to="{ name: 'ressources' }">
            📚&nbsp;{{ $t('footer.resources') }}
          </router-link>
        </div>
        <!-- Right link -->
        <div class="col-sm" v-if="currentRoute !== 'quiz-detail'">
          <router-link :to="{ name: 'contribute' }">
            ✍️&nbsp;{{ $t('footer.contribute') }}
          </router-link>
        </div>
        <div class="col-sm" v-if="currentRoute === 'quiz-detail'">
          <router-link :to="{ name: 'quiz-list' }">
            🕹&nbsp;{{ $t('messages.allQuizs') }}
          </router-link>
          <br />
        </div>
      </div>

      <div class="row">
        <div class="col-sm">
          <a class="no-after" v-bind:href="configuration.application_linkedin_url" target="_blank"><img height="30px" src="/openmoji_linkedin_E046.svg" alt="Linkedin" title="Linkedin" /></a>
          <a class="no-after" v-bind:href="configuration.application_twitter_url" target="_blank"><img height="30px" src="/openmoji_twitter_E040.svg" alt="Twitter" title="Twitter" /></a>
          <a class="no-after" v-bind:href="configuration.application_facebook_url" target="_blank"><img height="30px" src="/openmoji_facebook_E042.svg" alt="Facebook" title="Facebook" /></a>
        </div>
        <div class="col-sm">
          <select v-model="$i18n.locale">
            <option v-for="(lang, i) in languages" :key="`Lang${i}`" :value="lang.key">
              {{ lang.value }}
            </option>
          </select>
        </div>
      </div>

      <div class="row" v-if="currentRoute === 'home' && configuration.application_frontend_ecoindex_url">
        <div class="col-sm">
          Cette page a un score <a v-bind:href="configuration.application_frontend_ecoindex_url" target="_blank">EcoIndex.fr</a> de
          <span class="ecoindex-score">80.2 / 100</span><span class="ecoindex-letter">A</span>
          <br class="d-sm-none" />
          Elle pèse 751 Ko et a demandé 11 requêtes.
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

  data() {
    return {
      languages: [
        { key: 'fr', value: '🇫🇷 Français' },
        { key: 'en', value: '🌐 English' },
      ],
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
};
</script>

<style scoped>
footer {
  background-color: #e9ecef;
  margin-top: 20px;
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

span.ecoindex-score {
  background-color: #6E9A1D;
  color: #fff;
  border: 3px solid #6E9A1D;
  border-radius: 14px;
  white-space: nowrap;
  /* font-weight: 500; */
  /* font-size: 15px; */
  padding: 0px 6px;
}
span.ecoindex-letter {
  background-color: #349a47;
  color: #fff;
  border: 5px solid #e9ecef; /* same as footer */
  border-radius: 25px;
  white-space: nowrap;
  /* font-weight: 700; */
  /* font-size: 18px; */
  margin-left: -6px;
  padding: 2px 6px;
}
</style>
