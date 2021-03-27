<template>
  <section class="filter-box" :class="{ 'background-color-dark-grey': showFilterBox }">

    <!-- Header -->
    <div class="filter-box--header">

      <div class="row no-gutters">
        <div class="col-3 text-align-left">
          <span class="label label-hidden"><strong>{{ counter }}</strong> {{ objectType }}{{ (objectType === 'question' && questionsDisplayedCount > 1) ? 's' : '' }}</span>
        </div>

        <div class="col-6 text-center">
          <span v-for="(value, key) in questionFilters" :key="key">
            <FilterLabel v-if="key !== 'sort' && questionFilters[key]" :filterType="key" :filterValue="value" :showCross="true" @filter-label-clicked="removeFilter"></FilterLabel>
          </span>
        </div>

        <div class="col-3 text-align-right cursor-pointer" @click="toggleFilterBox()">
          <span class="label label-hidden">
            <img height="25px" src="/openmoji_filter_E257.svg" :alt="$t('messages.filters')" :title="$t('messages.filters')" />
            <img height="25px" src="/openmoji_sort_E265.svg" :alt="$t('messages.sort')" :title="$t('messages.sort')" />
            <span v-if="!showFilterBox">&nbsp;▸</span> <!-- ▲ ► -->
            <span v-if="showFilterBox">&nbsp;▾</span> <!-- ▼ -->
          </span>
        </div>
      </div>

    </div>

    <!-- Content -->
    <section v-if="showFilterBox" class="filter-box--content">

      <div class="row">
        <div class="col-sm-6">
          <h6>
            <img height="20px" src="/openmoji_filter_E257.svg" :alt="$t('messages.filters')" :title="$t('messages.filters')" />
            {{ $t('messages.filters') }}
          </h6>
          <p v-if="categories && objectType =='question'">
            <span>{{ $t('messages.category') }}{{ $t('words.semiColon') }}&nbsp;</span>
            <select v-model="tempQuestionFilters['category']">
              <option v-for="(option, i) in tags" :key="i" :value="option.name">
                  {{ option.name }} ({{ option[objectType === 'question' ? 'question_count' : 'quiz_count'] }})
                </option>
            </select>
          </p>
          <p v-if="tags">
            <span>{{ $t('messages.tag') }}{{ $t('words.semiColon') }}&nbsp;</span>
            <select v-model="tempQuestionFilters['tag']">
              <option v-for="(option, i) in tags" :key="i" :value="option.name">
                  {{ option.name }} ({{ option[objectType === 'question' ? 'question_count' : 'quiz_count'] }})
                </option>
            </select>
          </p>
          <p v-if="authors">
            <span>{{ $t('messages.author') }}{{ $t('words.semiColon') }}&nbsp;</span>
            <select v-model="tempQuestionFilters['author']">
              <option v-for="(option, i) in authors" :key="i" :value="option.name">
                {{ option.name }} ({{ option[objectType === 'question' ? 'question_count' : 'quiz_count'] }})
              </option>
            </select>
          </p>
          <p v-if="difficultyLevels && objectType =='question'">
            <span>{{ $t('messages.difficulty') }}{{ $t('words.semiColon') }}&nbsp;</span>
            <select v-model="tempQuestionFilters['difficulty']">
              <option v-for="(option, i) in difficultyLevels" :key="i" :value="option.name">
                {{ option.name }} ({{ option[objectType === 'question' ? 'question_count' : 'quiz_count'] }})
              </option>
            </select>
          </p>
        </div>

        <div class="col-sm-6">
          <h6>
            <img height="20px" src="/openmoji_sort_E265.svg" :alt="$t('messages.sort')" :title="$t('messages.sort')" />
            {{ $t('messages.sort') }}
          </h6>
          <p v-if="quizSortChoices && objectType =='quiz'">
            <select v-model="tempQuestionFilters['sort']">
              <option v-for="(option, i) in quizSortChoices" :key="i" :value="option.key">
                {{ option.value }}
              </option>
            </select>
          </p>
        </div>
      </div>
    </section>

    <!-- Action Buttons -->
    <section v-if="showFilterBox" class="filter-box--action">
      <button class="btn btn-sm btn-outline-secondary margin-5" @click="clearQuestionFilters()">{{ $t('messages.reset') }}</button>
      <button class="btn btn-sm btn-outline-dark margin-5" @click="toggleFilterBox()">{{ $t('messages.cancel') }}</button>
      <button class="btn btn-sm margin-5" :class="JSON.stringify(questionFilters) === JSON.stringify(tempQuestionFilters) ? 'btn-outline-primary' : 'btn-primary'" @click="updateQuestionFilters(true)">{{ $t('messages.update') }}{{ $t('words.exclamationMark') }}</button>
    </section>

  </section>
</template>

<script>
import constants from '../constants';
import FilterLabel from './FilterLabel.vue';

export default {
  name: 'QuestionFilter',
  props: {
    objectType: { type: String, default: 'question' },
    counter: { type: Number, default: 0 },
  },
  components: {
    FilterLabel,
  },

  data() {
    return {
      tempQuestionFilters: {
        category: null,
        tag: null,
        author: null,
        difficulty: null,
        sort: constants.QUIZ_SORT_DEFAULT,
      },
      quizSortChoices: constants.QUIZ_SORT_CHOICE_LIST,
      showFilterBox: false,
    };
  },

  computed: {
    categories() {
      return this.$store.state.categories;
    },
    tags() {
      return this.$store.state.tags
        .slice(0) // .slice makes a copy of the array, instead of mutating the orginal
        .filter((t) => {
          return (this.objectType === 'question') ? t.question_count : t.quiz_count;
        })
        .sort((a, b) => a.name.localeCompare(b.name));
    },
    authors() {
      return this.$store.state.authors
        .slice(0) // .slice makes a copy of the array, instead of mutating the orginal
        .filter((a) => {
          return (this.objectType === 'question') ? a.question_count : a.quiz_count;
        })
        .sort((a, b) => {
          return (this.objectType === 'question') ? (b.question_count - a.question_count) : (b.quiz_count - a.quiz_count);
        });
    },
    difficultyLevels() {
      return this.$store.state.difficultyLevels;
    },
    questionFilters() {
      return this.$store.state.questionFilters;
    },
    questionsDisplayedCount() {
      return this.$store.state.questionsDisplayed.length;
    },
    quizzes() {
      return this.$store.state.quizzes;
    },
  },

  watch: {
    // eslint-disable-next-line
    objectType (newType, oldType) {
      this.updateQuestionFilters();
    },
    quizzes() {
      // We need to updateFilter because sometimes the quizzes
      // or questions doen't exist in mounted
      this.updateQuestionFilters();
    },
  },

  mounted() {
    if (Object.keys(this.$route.query).length) {
      Object.keys(this.$route.query).forEach((key) => {
        if (this.$route.query[key] !== null) {
          this.tempQuestionFilters[key] = this.$route.query[key];
        }
      });
    }
    this.updateQuestionFilters();
  },

  methods: {
    toggleFilterBox() {
      this.showFilterBox = !this.showFilterBox;
      this.tempQuestionFilters = { ...this.questionFilters };
    },
    updateTempQuestionFilter(data) {
      this.tempQuestionFilters[data.key] = (this.tempQuestionFilters[data.key] === data.value) ? null : data.value;
    },
    clearQuestionFilters() {
      this.$router.push({ query: {} });
      this.tempQuestionFilters = {
        category: null,
        tag: null,
        author: null,
        difficulty: null,
        sort: constants.QUIZ_SORT_DEFAULT,
      };
      this.updateQuestionFilters();
    },
    updateQuestionFilters(updateQueryParams = false) {
      if (updateQueryParams) {
        this.updateQuestionFiltersAndQueryParams();
      }
      this.showFilterBox = false;
      if (this.objectType === 'question') {
        this.$store.dispatch('UPDATE_QUESTION_FILTERS', this.tempQuestionFilters);
      } else {
        this.$store.dispatch('UPDATE_QUIZ_FILTERS', this.tempQuestionFilters);
      }
    },
    removeFilter(data) {
      this.tempQuestionFilters[data.key] = null;
      this.updateQuestionFilters(true);
    },
    updateQuestionFiltersAndQueryParams() {
      const query = {};
      Object.keys(this.tempQuestionFilters).forEach((key) => {
        if (this.tempQuestionFilters[key] !== null) {
          query[key] = this.tempQuestionFilters[key];
        }
      });
      this.$router.push({ query });
    },
  },
};
</script>

<style scoped>
.filter-box {
  /* background-color: #ebebeb; */
  /* box-shadow: 0px 0px 5px 5px #c5c5c5;
  border-radius: 5px; */
  margin: 5px 0px;
  padding: 0px 5px;
}
.filter-box > .filter-box--content {
  background-color: white;
  max-height: 50vh;
  overflow-x: hidden;
  overflow-y: scroll;
}
.filter-box > .filter-box--action {
  padding-top: 5px;
}

select {
  max-width: 200px;
}
</style>
