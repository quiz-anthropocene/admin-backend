<template>
  <section class="text-align-left">
    <h2>Quelques statistiques</h2>

    <p class="text-muted">Mise à jour : {{ data_last_updated }}</p>

    <br />
    <h3>🕹️&nbsp;Quizs</h3>
    <p>
      <strong>{{ quiz_count_formatted }}</strong> publiés.
      <br />
      <strong>{{ quiz_answer_count_formatted }}</strong> quizs terminés depuis le lancement
      (dont <strong>{{ quiz_answer_count_last_30_days_formatted }}</strong> durant les 30 derniers jours).
    </p>

    <br />
    <h3>❓&nbsp;Questions</h3>
    <p>
      <strong>{{ question_validated_count_formatted }}</strong> validées,
      et <strong>{{ question_pending_validation_count_formatted }}</strong> en cours de validation.
      <br />
      <strong>{{ question_answer_count_formatted }}</strong> questions répondues depuis le lancement
      (dont <strong>{{ question_answer_count_last_30_days_formatted }}</strong> durant les 30 derniers jours).
    </p>

    <br />
    <h3>❓&nbsp;Contributions</h3>
    <p>
      <strong>{{ feedback_agg_formatted }}</strong> feedbacks/likes/suggestions reçus, merci ! 💯
    </p>

    <br />
    <hr />
    <br />

    <h3>Toutes les questions par...</h3>
    <p><i>Cliquez sur une bulle pour voir toutes les questions (validées) associées.</i></p>

    <br />
    <h4>📂&nbsp;Catégories</h4>
    <p>
      <span v-for="category in categories" :key="category.name">
        <router-link class="no-decoration" :to="{ name: 'question-list', query: { category: category.name } }">
          <FilterLabel filterType="category" v-bind:filterObject="category" />
        </router-link>
      </span>
    </p>

    <br />
    <h4>🏷️&nbsp;Tags</h4>
    <p :class="{ 'max-height-300': !showAllTags }">
      <span v-for="tag in tags" :key="tag.name">
        <router-link class="no-decoration" :to="{ name: 'question-list', query: { tag: tag.name } }">
          <FilterLabel :key="tag.name" filterType="tag" v-bind:filterObject="tag" />
        </router-link>
      </span>
    </p>
    <p class="text-center fake-link">
      <span @click="toggleAllTags()">
        <span v-if="!showAllTags">Afficher tous les tags</span>
        <span v-if="showAllTags">Cacher tous les tags</span>
      </span>
    </p>

    <br />
    <h4>✍️&nbsp;Auteurs</h4>
    <p>
      <span v-for="author in authors" :key="author.name">
        <router-link class="no-decoration" :to="{ name: 'question-list', query: { author: author.name } }">
          <FilterLabel :key="author.name" filterType="author" v-bind:filterObject="author" />
        </router-link>
      </span>
    </p>

    <br />
    <h4>🏆&nbsp;Niveaux de difficulté</h4>
    <p>
      <span v-for="difficulty in difficultyLevels" :key="difficulty.name">
        <router-link class="no-decoration" :to="{ name: 'question-list', query: { difficulty: difficulty.value } }">
          <FilterLabel :key="difficulty.name" filterType="difficulty" v-bind:filterObject="difficulty" />
        </router-link>
      </span>
    </p>

  </section>
</template>

<script>
import constants from '../constants';
import { metaTagsGenerator } from '../utils';
import FilterLabel from '../components/FilterLabel.vue';

export default {
  name: 'StatsPage',
  metaInfo() {
    const title = 'Statistiques';
    return {
      meta: metaTagsGenerator(title),
    };
  },
  components: {
    FilterLabel,
  },

  data() {
    return {
      showAllTags: false,
    };
  },

  computed: {
    data_last_updated() {
      return new Date(constants.DATA_LAST_UPDATED_DATETIME).toLocaleDateString('fr-FR', { year: 'numeric', month: 'long', day: 'numeric' });
    },
    question_validated_count_formatted() {
      const questionValidatedCount = this.$store.state.stats.question_per_validation_status_count ? this.$store.state.stats.question_per_validation_status_count.slice(0).find((item) => item.validation_status === constants.QUESTION_VALIDATION_STATUS_OK).total : 0;
      return Intl.NumberFormat('fr-FR').format(questionValidatedCount);
    },
    question_pending_validation_count_formatted() {
      const questionPendingValidationCount = this.$store.state.stats.question_per_validation_status_count ? this.$store.state.stats.question_per_validation_status_count.slice(0).find((item) => item.validation_status === constants.QUESTION_VALIDATION_STATUS_IN_PROGRESS).total : 0;
      return Intl.NumberFormat('fr-FR').format(questionPendingValidationCount);
    },
    quiz_count_formatted() {
      return Intl.NumberFormat('fr-FR').format(this.$store.state.quizzes.length);
    },
    question_answer_count_formatted() {
      return Intl.NumberFormat('fr-FR').format(this.$store.state.stats.question_answer_count);
    },
    quiz_answer_count_formatted() {
      return Intl.NumberFormat('fr-FR').format(this.$store.state.stats.quiz_answer_count);
    },
    question_answer_count_last_30_days_formatted() {
      return Intl.NumberFormat('fr-FR').format(this.$store.state.stats.question_answer_count_last_30_days);
    },
    quiz_answer_count_last_30_days_formatted() {
      return Intl.NumberFormat('fr-FR').format(this.$store.state.stats.quiz_answer_count_last_30_days);
    },
    feedback_agg_formatted() {
      const feedbackAgg = this.$store.state.stats.question_feedback_count + this.$store.state.stats.quiz_feedback_count + this.$store.state.stats.contribution_count;
      return Intl.NumberFormat('fr-FR').format(feedbackAgg);
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
  },

  mounted() {
    this.$store.dispatch('GET_STATS_DICT_FROM_LOCAL_YAML');
  },

  methods: {
    toggleAllTags() {
      this.showAllTags = !this.showAllTags;
    },
  },
};
</script>
