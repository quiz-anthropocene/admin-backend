<template>
  <section class="text-align-left">
    <h2>Quelques statistiques</h2>
    
    <h3>❓&nbsp;Questions</h3>
    <p>
      Il y a actuellement <strong v-if="questionPublishCount">{{ questionPublishCount }}</strong> questions publiées,
      et <strong v-if="questionValidationStatusInProgressCount">{{ questionValidationStatusInProgressCount }}</strong> en cours de validation.
    </p>

    <br />
    <h3>🕹️&nbsp;Quiz</h3>
    <p>
      <strong v-if="quizPublishStats">{{ quizPublishStats[0]["count"] }}</strong> quiz ont été créés.
    </p>

    <br />
    <h3>🔗&nbsp;Réponses</h3>
    <p>
      L'application totalise <strong>{{ questionAnswerCountStats }}</strong> réponses (depuis la mise en ligne en Mars 2020).
    </p>

    <br />
    <h3>📂&nbsp;Catégories</h3>
    Questions par catégories:
    <ul>
      <li v-for="categoryStat in questionCategoryStats" :key="categoryStat.name">
        {{ categoryStat.name }}: <strong>{{ categoryStat.count }}</strong>
      </li>
    </ul>

    <br />
    <h3>🏷️&nbsp;Tags</h3>
    Questions par tags:
    <ul>
      <li v-for="tagStat in questionTagStats" :key="tagStat.name">
        {{ tagStat.name }}: <strong>{{ tagStat.count }}</strong>
      </li>
    </ul>

    <br />
    <h3>✍️&nbsp;Auteurs</h3>
    Questions par auteurs:
    <ul>
      <li v-for="authorStat in questionAuthorStats" :key="authorStat.name">
        {{ authorStat.name }}: <strong>{{ authorStat.count }}</strong>
      </li>
    </ul>

  </section>
</template>

<script>
export default {
  name: 'StatsPage',
  components: {
  },

  data() {
    return {
      questionPublishCount: null,
      questionValidationStatusInProgressCount: null,
      quizPublishStats: null,
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
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/stats`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.questionPublishCount = data["question_publish_count"];
          this.questionValidationStatusInProgressCount = data["question_validation_status_in_progress_count"];
          this.quizPublishStats = data["quiz_publish"];
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
