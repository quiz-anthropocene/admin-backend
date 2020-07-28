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
    <p>
      <FilterLabel v-for="category in categories" :key="category.name" filterType="category" v-bind:filterObject="category" />
    </p>

    <br />
    <h3>🏷️&nbsp;Tags</h3>
    <p>
      <FilterLabel v-for="tag in tags" :key="tag.name" filterType="tag" v-bind:filterObject="tag" />
    </p>

    <br />
    <h3>✍️&nbsp;Auteurs</h3>
    <p>
      <FilterLabel v-for="author in authors" :key="author.name" filterType="author" v-bind:filterObject="author" />
    </p>

    <br />
    <h3>🏆&nbsp;Difficulté</h3>
    <p>
      <FilterLabel v-for="difficulty in difficultyLevels" :key="difficulty.name" filterType="difficulty" v-bind:filterObject="difficulty" />
    </p>

  </section>
</template>

<script>
import FilterLabel from '../components/FilterLabel.vue';

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
    FilterLabel,
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
    difficultyLevels() {
      return this.$store.state.difficultyLevels;
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
