<template>
  <section class="text-align-left">
    <h2>Quelques statistiques</h2>

    <p class="text-muted">Mise à jour : 17 Juillet 2020</p>

    <br />
    <h3>❓&nbsp;Questions</h3>
    <p>
      Il y a actuellement <strong>{{ question_count }}</strong> questions publiées,
      et <strong>{{ question_pending_validation_count }}</strong> en cours de validation.
    </p>

    <br />
    <h3>🕹️&nbsp;Quiz</h3>
    <p>
      <strong>{{ quiz_count ? quiz_count : 0 }}</strong> quiz ont été publiés.
    </p>

    <br />
    <h3>🔗&nbsp;Réponses</h3>
    <p>
      L'application totalise <strong v-if="stats.total">{{ stats.total.question_answer_count }}</strong> réponses (depuis la mise en ligne en Mars 2020).
    </p>

    <br />
    <h3>📂&nbsp;Catégories</h3>
    Questions par catégories:
    <ul>
      <li v-for="category in categories" :key="category.name">
        {{ category.name }}: <strong>{{ category.question_count }}</strong>
      </li>
    </ul>

    <br />
    <h3>🏷️&nbsp;Tags</h3>
    Questions par tags:
    <ul>
      <li v-for="tag in tags" :key="tag.name">
        {{ tag.name }}: <strong>{{ tag.question_count }}</strong>
      </li>
    </ul>

    <br />
    <h3>✍️&nbsp;Auteurs</h3>
    Questions par auteurs:
    <ul>
      <li v-for="author in authors" :key="author.name">
        {{ author.name }}: <strong>{{ author.question_count }}</strong>
      </li>
    </ul>

  </section>
</template>

<script>
export default {
  name: 'StatsPage',
  metaInfo: {
    title: 'Statistiques',
    meta: [
      { property: 'og:title', vmid: 'og:title', content: 'Statistiques' },
      { property: 'twitter:title', vmid: 'twitter:title', content: 'Statistiques' },
    ],
  },
  components: {
  },

  data() {
    return {
      //
    };
  },

  computed: {
    question_count() {
      return this.$store.state.questions.length;
    },
    question_pending_validation_count() {
      return this.$store.state.questionsPendingValidation.length;
    },
    quiz_count() {
      return this.$store.state.quizzes.length;
    },
    categories() {
      return this.$store.state.categories
        .filter((c) => c.question_count)
        .sort((a, b) => b.question_count - a.question_count);
    },
    tags() {
      return this.$store.state.tags
        .filter((t) => t.question_count)
        .sort((a, b) => b.question_count - a.question_count);
    },
    authors() {
      return this.$store.state.authors
        .filter((a) => a.question_count)
        .sort((a, b) => b.question_count - a.question_count);
    },
    stats() {
      return this.$store.state.stats;
    },
  },

  mounted() {
    this.fetchQuestionStats();
  },

  methods: {
    fetchQuestionStats() {
      this.$store.dispatch('GET_STATS');
    },

  },
};
</script>
