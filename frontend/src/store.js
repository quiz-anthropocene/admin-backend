import Vue from 'vue';
import Vuex from 'vuex';

import glossaryYamlData from './data/glossary.yaml';

Vue.use(Vuex);

const jsyaml = require('js-yaml');

function processModelList(data) {
  const dataFix = JSON.parse(JSON.stringify(data)); // fix for local imports ?
  console.log('processModelList', data);
  dataFix.map((el) => {
    // move 'fields' key up
    // Object.keys(el.fields).forEach((f) => { el[f] = el.fields[f]; });
    const elmerged = { ...el, ...el.fields };
    delete el.fields;
    // add 'id' key
    elmerged.id = el.pk;
    return elmerged;
  });
  console.log('dataFix', dataFix);
  return dataFix;
}

/**
 * goal: process raw yaml files
 * input: text file (with 'pk' & 'fields' fields)
 * output: json object
 */
function processYamlFile(dataYaml) {
  console.log('processYamlFile', dataYaml);
  const data = jsyaml.load(dataYaml); // safeLoad + try/catch
  return processModelList(data);
}

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
    glossary: [],
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
        .then((dataJson) => {
          commit('SET_QUESTION_LIST', { list: dataJson });
          // commit('UPDATE_QUESTIONS_DISPLAYED')
          // document.dispatchEvent(new Event('custom-render-trigger'));
        })
        .catch((error) => {
          commit('UPDATE_LOADING_STATUS', false);
          commit('UPDATE_ERROR', error);
          console.log(error);
        });
    },
    GET_QUESTION_LIST_FROM_YAML: ({ commit }) => {
      commit('UPDATE_LOADING_STATUS', true);
      commit('UPDATE_ERROR', null);
      fetch('https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/questions.yaml')
        .then((response) => {
          commit('UPDATE_LOADING_STATUS', false);
          commit('UPDATE_ERROR', null);
          response.text();
        })
        .then((dataYaml) => {
          commit('SET_QUESTION_LIST', { list: processYamlFile(dataYaml) }); // filter
          // document.dispatchEvent(new Event('custom-render-trigger'));
        })
        .catch((error) => {
          commit('UPDATE_LOADING_STATUS', false);
          commit('UPDATE_ERROR', error);
          console.log(error);
          // this.error = error;
        });
    },
    GET_QUIZ_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/quizzes`)
        .then((response) => response.json())
        .then((dataJson) => {
          commit('SET_QUIZ_LIST', { list: dataJson });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_QUIZ_LIST_FROM_YAML: ({ commit }) => {
      fetch('https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/quizzes.yaml')
        .then((response) => response.text())
        .then((dataYaml) => {
          commit('SET_QUIZ_LIST', { list: processYamlFile(dataYaml) }); // full ?
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_CATEGORY_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/categories`)
        .then((response) => {
          console.log(response);
          response.json();
        })
        .then((dataJson) => {
          commit('SET_CATEGORY_LIST', { list: dataJson });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_CATEGORY_LIST_FROM_YAML: ({ commit }) => {
      fetch('https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/categories.yaml')
        .then((response) => response.text())
        .then((dataYaml) => {
          commit('SET_CATEGORY_LIST', { list: processYamlFile(dataYaml) });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_TAG_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/tags`)
        .then((response) => response.json())
        .then((dataJson) => {
          commit('SET_TAG_LIST', { list: dataJson });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_TAG_LIST_FROM_YAML: ({ commit }) => {
      fetch('https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/tags.yaml')
        .then((response) => response.text())
        .then((dataYaml) => {
          commit('SET_TAG_LIST', { list: processYamlFile(dataYaml) });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_AUTHOR_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/authors`)
        .then((response) => response.json())
        .then((dataJson) => {
          commit('SET_AUTHOR_LIST', { list: dataJson });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_DIFFICULTY_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/difficulty-levels`)
        .then((response) => response.json())
        .then((dataJson) => {
          commit('SET_DIFFICULTY_LEVEL_LIST', { list: dataJson });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_GLOSSARY_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/glossary`)
        .then((response) => response.json())
        .then((dataJson) => {
          commit('SET_GLOSSARY_LIST', { list: dataJson });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_GLOSSARY_LIST_FROM_YAML: ({ commit }) => {
      fetch('https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/glossary.yaml')
        .then((response) => response.text())
        .then((dataYaml) => {
          commit('SET_GLOSSARY_LIST', { list: processYamlFile(dataYaml) });
          // document.dispatchEvent(new Event('custom-render-trigger'));
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_GLOSSARY_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      // console.log("GET_GLOSSARY_LIST_FROM_LOCAL_YAML", glossaryYamlData, data)
      // commit('SET_GLOSSARY_LIST', { list: processModelList(glossaryYamlData) });
      commit('SET_GLOSSARY_LIST', { list: glossaryYamlData });
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
    SET_GLOSSARY_LIST: (state, { list }) => {
      state.glossary = list;
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
    getQuestionByIdList: (state) => (questionIdList) => state.questions.filter((q) => (questionIdList.includes(q.id))),
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
    getQuizById: (state, getters) => (quizId, full = false) => {
      const quiz = state.quizzes.find((q) => (q.id === quizId));
      if (quiz && full) {
        // replace the quiz's list of question ids with a list of question objects
        const quizQuestionsListFull = getters.getQuestionByIdList(quiz.questions);
        if (quizQuestionsListFull.length === quiz.questions.length) {
          quiz.questions = quizQuestionsListFull;
        }
      }
      return quiz;
    },
  },
});

export default store;
