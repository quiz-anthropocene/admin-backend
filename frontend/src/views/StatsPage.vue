<template>
  <section class="text-align-left">
    <h2>Quelques statistiques</h2>
    
    <h3>Questions</h3>
    <p>
      Il y a actuellement <strong v-if="questionPublishStats">{{ questionPublishStats[0]["count"] }}</strong> questions publiées,
      et <strong v-if="questionPublishStats">{{ questionPublishStats[1]["count"] }}</strong> en cours de validation.
    </p>

    <br />
    <h3>Réponses</h3>
    <p>
      L'application totalise <strong>{{ questionAnswerCountStats }}</strong> réponses (depuis la mise en ligne en Mars 2020).
    </p>

    <br />
    <h3>Catégories</h3>
    Questions par catégories:
    <ul>
      <li v-for="categoryStat in questionCategoryStats" :key="categoryStat.name">
        {{ categoryStat["name"] }}: <strong>{{ categoryStat["count"] }}</strong>
      </li>
    </ul>

    <br />
    <h3>Tags</h3>
    Questions par tags:
    <ul>
      <li v-for="tagStat in questionTagStats" :key="tagStat.name">
        {{ tagStat["name"] }}: <strong>{{ tagStat["count"] }}</strong>
      </li>
    </ul>

    <br />
    <h3>Auteurs</h3>
    Questions par auteurs:
    <ul>
      <li v-for="authorStat in questionAuthorStats" :key="authorStat.name">
        {{ authorStat["author"] }}: <strong>{{ authorStat["count"] }}</strong>
      </li>
    </ul>
    
    <br />
    <hr />
    <div class="row actions text-center">
      <div class="col-sm"></div>
      <div class="col-sm">
        <router-link :to="{ name: 'about' }">
          ℹ️&nbsp;À propos de cette application
        </router-link>
        <br />
      </div>
      <div class="col-sm">
        <HomeLink />
      </div>
    </div>
  </section>
</template>

<script>
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'StatsPage',
  components: {
    HomeLink,
  },

  data() {
    return {
      questionPublishStats: null,
      questionAnswerCountStats: null,
      questionCategoryStats: null,
      questionTagStats: null,
      questionAuthorStats: null,
      // questionAnswerStats: null,
      loading: false,
      error: null,
    }
  },

  mounted () {
    this.fetchQuestionStats();
  },

  methods: {
    fetchQuestionStats() {
      this.error = this.question = null;
      this.loading = true;
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions/stats`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.questionPublishStats = data["publish"];
          this.questionAnswerCountStats = data["answer_count"];
          this.questionCategoryStats = data["category"];
          this.questionTagStats = data["tag"];
          this.questionAuthorStats = data["author"];
          // this.questionAnswerStats = data["answer"];
          
        })
        .catch(error => {
          console.log(error)
          this.error = error;
        })
    },

  }
}
</script>
