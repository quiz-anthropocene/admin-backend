<template>
  <section class="text-align-left">
    <h2>Quelques statistiques</h2>

    <section v-if="$i18n.locale === 'en'" class="alert alert-warning" role="alert">
      🌐Page not yet translated
    </section>

    <p class="text-muted">Mise à jour : {{ data_last_updated }}</p>

    <br />
    <h3>🕹️&nbsp;Quizs</h3>
    <p>
      <strong>{{ quiz_published_count_formatted }}</strong> publiés.
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
    <h3>✍️&nbsp;Contributions</h3>
    <p>
      <strong>{{ feedback_agg_formatted }}</strong> feedbacks/likes/suggestions reçus, merci ! 💯
    </p>

    <br />
    <hr />
    <br />

    <h3>{{ $t('messages.allQuizs') }} {{ $t('words.by') }}...</h3>
    <p><i>Cliquez sur une bulle pour voir tous les quizs (publiés) associés.</i></p>

    <br />
    <h4>🏷️&nbsp;{{ $t('messages.tags') }}</h4>
    <p>
      <span v-for="tag in quizTags" :key="tag.name">
        <router-link class="no-decoration" :to="{ name: 'quiz-list', query: { tag: tag.name } }">
          <FilterLabel :key="tag.name" filterType="tag" v-bind:filterValue="tag.name" v-bind:filterCount="tag.quiz_count" />
        </router-link>
      </span>
    </p>

    <br />
    <h4>✍️&nbsp;{{ $t('messages.authors') }}</h4>
    <p>
      <span v-for="author in quizAuthors" :key="author.id">
        <router-link class="no-decoration" :to="{ name: 'quiz-list', query: { author: author.id } }">
          <FilterLabel :key="author.id" filterType="author" v-bind:filterValue="author.first_name + ' ' + author.last_name" v-bind:filterCount="author.quiz_count" />
        </router-link>
      </span>
    </p>

    <br />
    <h4>🌐&nbsp;{{ $t('messages.languages') }}</h4>
    <p>
      <span v-for="language in languages" :key="language.name">
        <!-- <router-link class="no-decoration" :to="{ name: 'quiz-list', query: { locale: language.key } }"> -->
          <FilterLabel :key="language.name" filterType="language" v-bind:filterValue="language.name" v-bind:filterCount="language.quiz_count" v-bind:withHover="false" />
        <!-- </router-link> -->
      </span>
    </p>

    <br />
    <hr />
    <br />

    <h3>{{ $t('messages.allQuestions') }} {{ $t('words.by') }}...</h3>
    <p><i>Cliquez sur une bulle pour voir toutes les questions (validées) associées.</i></p>

    <br />
    <h4>📂&nbsp;{{ $t('messages.categories') }}</h4>
    <p>
      <span v-for="category in categories" :key="category.name">
        <router-link class="no-decoration" :to="{ name: 'question-list', query: { category: category.name } }">
          <FilterLabel filterType="category" v-bind:filterValue="category.name" v-bind:filterCount="category.question_count" />
        </router-link>
      </span>
    </p>

    <br />
    <h4>🏷️&nbsp;{{ $t('messages.tags') }}</h4>
    <p :class="{ 'max-height-300': !showAllQuestionTags }">
      <span v-for="tag in questionTags" :key="tag.name">
        <router-link class="no-decoration" :to="{ name: 'question-list', query: { tag: tag.name } }">
          <FilterLabel :key="tag.name" filterType="tag" v-bind:filterValue="tag.name" v-bind:filterCount="tag.question_count" />
        </router-link>
      </span>
    </p>
    <p class="text-center fake-link">
      <span @click="toggleAllQuestionTags()">
        <span v-if="!showAllQuestionTags">{{ $t('stats.showAllTags') }}</span>
        <span v-if="showAllQuestionTags">{{ $t('stats.hideAllTags') }}</span>
      </span>
    </p>

    <br />
    <h4>✍️&nbsp;{{ $t('messages.authors') }}</h4>
    <p>
      <span v-for="author in questionAuthors" :key="author.id">
        <router-link class="no-decoration" :to="{ name: 'question-list', query: { author: author.id } }">
          <FilterLabel :key="author.id" filterType="author" v-bind:filterValue="author.first_name + ' ' + author.last_name" v-bind:filterCount="author.question_count" />
        </router-link>
      </span>
    </p>

    <br />
    <h4>🏆&nbsp;{{ $t('messages.difficulty') }}</h4>
    <p>
      <span v-for="difficulty in difficultyLevels" :key="difficulty.name">
        <router-link class="no-decoration" :to="{ name: 'question-list', query: { difficulty: difficulty.value } }">
          <FilterLabel :key="difficulty.name" filterType="difficulty" v-bind:filterValue="difficulty.value" v-bind:filterCount="difficulty.question_count" />
        </router-link>
      </span>
    </p>

    <br />
    <h4>🌐&nbsp;{{ $t('messages.languages') }}</h4>
    <p>
      <span v-for="language in languages" :key="language.name">
        <!-- <router-link class="no-decoration" :to="{ name: 'question-list', query: { locale: language.key } }"> -->
          <FilterLabel :key="language.name" filterType="language" v-bind:filterValue="language.name" v-bind:filterCount="language.question_count" v-bind:withHover="false" />
        <!-- </router-link> -->
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
      showAllQuestionTags: false,
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
      const questionPendingValidation = this.$store.state.stats.question_per_validation_status_count ? this.$store.state.stats.question_per_validation_status_count.slice(0).find((item) => item.validation_status === constants.QUESTION_VALIDATION_STATUS_IN_PROGRESS) : {};
      const questionPendingValidationCount = questionPendingValidation ? questionPendingValidation.total : 0;
      return Intl.NumberFormat('fr-FR').format(questionPendingValidationCount);
    },
    quiz_published_count_formatted() {
      const quizPublishedCount = this.$store.state.stats.quiz_per_publish_count ? this.$store.state.stats.quiz_per_publish_count.slice(0).find((item) => item.publish === true).total : 0;
      return Intl.NumberFormat('fr-FR').format(quizPublishedCount);
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
    quizTags() {
      return this.$store.state.tags
        .filter((t) => t.quiz_count)
        .sort((a, b) => b.quiz_count - a.quiz_count);
    },
    questionTags() {
      return this.$store.state.tags
        .filter((t) => t.question_count)
        .sort((a, b) => b.question_count - a.question_count);
    },
    quizAuthors() {
      return this.$store.state.authors
        .filter((a) => a.quiz_count)
        .sort((a, b) => b.quiz_count - a.quiz_count);
    },
    questionAuthors() {
      return this.$store.state.authors
        .filter((a) => a.question_count)
        .sort((a, b) => b.question_count - a.question_count);
    },
    difficultyLevels() {
      return this.$store.state.difficultyLevels;
    },
    languages() {
      return this.$store.state.languages;
    },
  },

  mounted() {
    this.$store.dispatch('GET_STATS_DICT_FROM_LOCAL_YAML');
  },

  methods: {
    toggleAllQuestionTags() {
      this.showAllQuestionTags = !this.showAllQuestionTags;
    },
  },
};
</script>
