import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    loading: true,
    error: null,
    questions: [], // received in random order
    questionsDisplayed: [],
    quizzes: [],
    categories: [],
    tags: [],
    authors: [],
    difficultyLevels: [],
    questionFilters: {
      category: null,
      tag: null,
      author: null,
      difficulty: null,
    },
  },
  actions: {
    GET_QUESTION_LIST: ({ commit }) => {
      commit('UPDATE_LOADING_STATUS', true);
      commit('UPDATE_ERROR', null);
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions`)
        .then((response) => {
          commit('UPDATE_LOADING_STATUS', false);
          commit('UPDATE_ERROR', null);
          return response.json();
        })
        .then((data) => {
          commit('SET_QUESTION_LIST', { list: data });
          // commit('UPDATE_QUESTIONS_DISPLAYED')
        })
        .catch((error) => {
          commit('UPDATE_LOADING_STATUS', false);
          commit('UPDATE_ERROR', error);
          console.log(error);
        });
    },
    GET_QUIZ_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/quizzes?full=true`)
        .then((response) => {
          // this.loading = false
          response.json();
        })
        .then((data) => {
          commit('SET_QUIZ_LIST', { list: data });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_CATEGORY_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/categories`)
        .then((response) => {
          // this.loading = false
          response.json();
        })
        .then((data) => {
          commit('SET_CATEGORY_LIST', { list: data });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_TAG_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/tags`)
        .then((response) => {
          // this.loading = false
          response.json();
        })
        .then((data) => {
          commit('SET_TAG_LIST', { list: data });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_AUTHOR_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/authors`)
        .then((response) => {
          // this.loading = false
          response.json();
        })
        .then((data) => {
          commit('SET_AUTHOR_LIST', { list: data });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_DIFFICULTY_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/difficulty-levels`)
        .then((response) => {
          // this.loading = false
          response.json();
        })
        .then((data) => {
          commit('SET_DIFFICULTY_LEVEL_LIST', { list: data });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    UPDATE_QUESTION_FILTERS: ({ commit, state }, filterObject) => {
      const currentQuestionFilters = filterObject || state.questionFilters;
      commit('UPDATE_QUESTION_FILTERS', { filterObject: currentQuestionFilters });
      commit('UPDATE_QUESTIONS_DISPLAYED', { filterObject: currentQuestionFilters });
    },
  },
  mutations: {
    UPDATE_LOADING_STATUS: (state, value) => {
      state.loading = value;
    },
    UPDATE_ERROR: (state, value) => {
      state.error = value;
    },
    SET_QUESTION_LIST: (state, { list }) => {
      state.questions = list;
      state.questionsDisplayed = list;
      // TODO: state.authors & question_count
      // TODO: state.difficulty & question_count
    },
    SET_QUIZ_LIST: (state, { list }) => {
      state.quizzes = list;
    },
    SET_CATEGORY_LIST: (state, { list }) => {
      state.categories = list;
    },
    SET_TAG_LIST: (state, { list }) => {
      state.tags = list;
    },
    SET_AUTHOR_LIST: (state, { list }) => {
      state.authors = list;
    },
    SET_DIFFICULTY_LEVEL_LIST: (state, { list }) => {
      state.difficultyLevels = list;
    },
    UPDATE_QUESTION_FILTERS: (state, { filterObject }) => {
      state.questionFilters = filterObject;
    },
    UPDATE_QUESTIONS_DISPLAYED: (state, { filterObject }) => {
      state.questionsDisplayed = state.questions
        .filter((q) => (filterObject.category ? (q.category === filterObject.category) : true))
        .filter((q) => (filterObject.tag ? q.tags.includes(filterObject.tag) : true))
        .filter((q) => (filterObject.author ? (q.author === filterObject.author) : true))
        .filter((q) => (filterObject.difficulty ? (q.difficulty === filterObject.difficulty) : true));
    },
  },
  getters: {
    getQuestionById: (state) => (questionId) => state.questions.find((q) => (q.id === questionId)),
    getQuestionsByCategoryName: (state) => (categoryName) => state.questions.filter((q) => (q.category === categoryName)),
    getQuestionsByTagName: (state) => (tagName) => state.questions.filter((q) => q.tags.includes(tagName)),
    getQuestionsByAuthorName: (state) => (authorName) => state.questions.filter((q) => q.author === authorName),
    getQuestionsByFilter: (state) => (filter) => state.questions.filter((q) => (filter.categoryName ? (q.category === filter.categoryName) : true))
      .filter((q) => (filter.tagName ? q.tags.includes(filter.tagName) : true))
      .filter((q) => (filter.authorName ? (q.author === filter.authorName) : true))
      .filter((q) => (filter.difficulty ? (q.difficulty === filter.difficulty) : true)),
    getCurrentQuestionIndex: (state) => (currentQuestionId) => state.questionsDisplayed.findIndex((q) => q.id === currentQuestionId),
    getNextQuestionByFilter: (state) => (currentQuestionId) => {
      const currentQuestionIndex = currentQuestionId ? state.questionsDisplayed.findIndex((q) => q.id === currentQuestionId) : state.questionsDisplayed[0];
      return state.questionsDisplayed[currentQuestionIndex + 1] ? state.questionsDisplayed[currentQuestionIndex + 1] : state.questionsDisplayed[0];
    },
    getQuizById: (state) => (quizId) => state.quizzes.find((q) => (q.id === quizId)),
  },
});

export default store;
