<template>
  <section class="small-container text-align-left">
    <h2>Quelques statistiques</h2>
    <h3>Questions</h3>
    <p>
      Il y a actuellement <strong>{{ questionPublishStats[0]["count"] }}</strong> questions publiées,
      et <strong>{{ questionPublishStats[1]["count"] }}</strong> en cours de rédaction/publication.
    </p>
    <h3>Catégories</h3>
    <i>Questions par catégories</i>
    <ul>
      <li v-for="categoryStat in questionCategoryStats" :key="categoryStat">{{ categoryStat["category"] }}: {{ categoryStat["count"] }}</li>
    </ul>
    <h3>Réponses</h3>
    <p>L'application totalise <strong>{{ questionAnswerCountStats }}</strong> réponses (depuis la mise en ligne le Lundi 9 Mars).</p>
    <h3>Contributions</h3>
    <p><i>à venir</i></p>

    <br />
    <br />
    <div class="home">
      <router-link :to="{ name: 'home' }">
        Retour au menu principal
      </router-link>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Stats',

  data() {
    return {
      questionPublishStats: null,
      questionCategoryStats: null,
      // questionAnswerStats: null,
      questionAnswerCountStats: null,
      loading: false,
      error: null,
    }
  },

  created () {
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
          this.questionCategoryStats = data["category"];
          // this.questionAnswerStats = data["answer"];
          this.questionAnswerCountStats = data["answer_count"];
        })
        .catch(error => {
          console.log(error)
          this.error = error;
        })
    },

  }
}
</script>