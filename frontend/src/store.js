import Vue from 'vue';
import Vuex from 'vuex';

import categoriesYamlData from '../../data/categories.yaml';
import tagsYamlData from '../../data/tags.yaml';
import questionsYamlData from '../../data/questions.yaml';
import quizzesYamlData from '../../data/quizzes.yaml';
import difficultyLevelsYamlData from '../../data/difficulty-levels.yaml';
import ressourcesGlossaireYamlData from '../../data/ressources-glossaire.yaml';
import ressourcesSoutiensYamlData from '../../data/ressources-soutiens.yaml';
import ressourcesAutresAppsYamlData from '../../data/ressources-autres-apps.yaml';

Vue.use(Vuex);

const jsyaml = require('js-yaml');

/**
 * goal: flatten json list of "django models"
 * input: array of objects, with 'pk' and 'fields' fields
 * output: array of objects with 'fields' object moved up
 */
function processModelList(data) {
  return data.map((el) => {
    Object.assign(el, { id: el.pk }, el.fields);
    return el;
  });
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
    loading: false,
    error: null,
    questions: [], // received in random order
    questionsDisplayed: [],
    questionsPendingValidation: [],
    questionFilters: {
      category: null,
      tag: null,
      author: null,
      difficulty: null,
    },
    quizzes: [],
    quizzesDisplayed: [],
    quizFilters: {
      tag: null,
    },
    categories: [],
    tags: [],
    authors: [],
    difficultyLevels: [],
    ressources: {
      glossaire: [],
      soutiens: [],
      autresApps: [],
    },
    stats: {},
  },
  actions: {
    RESET_LOADING_STATUS: ({ commit }) => {
      commit('UPDATE_LOADING_STATUS', false);
      commit('UPDATE_ERROR', null);
    },
    /**
     * Get questions
     */
    GET_QUESTION_LIST: ({ commit }) => {
      commit('UPDATE_LOADING_STATUS', true);
      commit('UPDATE_ERROR', null);
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions?full=true`)
        .then((response) => {
          commit('UPDATE_LOADING_STATUS', false);
          commit('UPDATE_ERROR', null);
          return response.json();
        })
        .then((dataJson) => {
          commit('SET_QUESTION_PUBLISHED_LIST', { list: dataJson });
          // commit('UPDATE_QUESTIONS_DISPLAYED')
          // document.dispatchEvent(new Event('custom-render-trigger'));
        })
        .catch((error) => {
          commit('UPDATE_LOADING_STATUS', false);
          commit('UPDATE_ERROR', error);
          console.log(error);
        });
    },
    GET_QUESTION_LIST_FROM_LOCAL_YAML: ({ commit, state, getters }) => {
      // questions
      const questionsPublished = processModelList(questionsYamlData)
        .filter((el) => el.publish === true)
        .sort(() => Math.random() - 0.5) // random order
        .sort((a, b) => a.difficulty - b.difficulty); // order by difficulty (easiest to hardest)
      const questionsPendingValidation = processModelList(questionsYamlData).filter((el) => el.validation_status === 'A valider');
      // questions: get category & tags objects
      questionsPublished.map((q) => {
        const questionCategory = getters.getCategoryById(q.category);
        const questionTags = getters.getTagsByIdList(q.tags);
        Object.assign(q, { category: questionCategory }, { tags: questionTags });
        return q;
      });
      commit('SET_QUESTION_PUBLISHED_LIST', { list: questionsPublished });
      commit('SET_QUESTION_PENDING_VALIDATION_LIST', { list: questionsPendingValidation });

      // update categories: add question_count
      state.categories.forEach((c) => {
        c.question_count = questionsPublished.filter((q) => q.category.name === c.name).length;
      });

      // update tags: add question_count
      state.tags.forEach((t) => {
        t.question_count = questionsPublished.filter((q) => q.tags.map((qt) => qt.id).includes(t.id)).length;
      });

      // create authors list: add question_count
      // TODO: use map/reduce instead
      const authors = [];
      questionsPublished.forEach((q) => {
        const authorListIndex = authors.map((a) => a.name).indexOf(q.author);
        if (authorListIndex >= 0) {
          authors[authorListIndex].question_count += 1;
        } else {
          authors.push({ name: q.author, question_count: 1 });
        }
      });
      commit('SET_AUTHOR_LIST', { list: authors });

      // create difficulty list: add question_count
      const difficultyLevels = difficultyLevelsYamlData;
      difficultyLevels.forEach((dl) => {
        dl.question_count = questionsPublished.filter((q) => q.difficulty === dl.value).length;
      });
      commit('SET_DIFFICULTY_LEVEL_LIST', { list: difficultyLevels });
    },
    /**
     * Get quizzes
     */
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
    GET_QUIZ_LIST_FROM_LOCAL_YAML: ({ commit, getters }) => {
      const quizPublished = processModelList(quizzesYamlData).filter((el) => el.publish === true);
      // quiz: get question objects, tag objects & difficulty average
      quizPublished.map((q) => {
        const quizQuestions = getters.getQuestionsByIdList(q.questions).sort(() => Math.random() - 0.5); // random order
        const quizTags = getters.getTagsByIdList(q.tags);
        const quizDifficultyAverage = quizQuestions.map((qq) => qq.difficulty).reduce((prev, curr) => prev + curr, 0) / quizQuestions.length;
        Object.assign(q, { questions: quizQuestions }, { tags: quizTags }, { difficulty_average: quizDifficultyAverage });
        return q;
      });
      commit('SET_QUIZ_LIST', { list: quizPublished });
    },
    /**
     * Get categories
     */
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
    GET_CATEGORY_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_CATEGORY_LIST', { list: processModelList(categoriesYamlData) });
    },
    /**
     * Get tags
     */
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
    GET_TAG_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      const tagsSorted = processModelList(tagsYamlData).sort((a, b) => a.name.localeCompare(b.name));
      commit('SET_TAG_LIST', { list: tagsSorted });
    },
    /**
     * Get authors
     */
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
    /**
     * Get difficulty list
     */
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
    /**
     * Get ressources: glossaire, soutiens, ...
     */
    GET_GLOSSARY_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/glossary`)
        .then((response) => response.json())
        .then((dataJson) => {
          commit('SET_RESSOURCES_GLOSSAIRE_LIST', { list: dataJson });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_RESSOURCES_GLOSSAIRE_LIST_FROM_YAML: ({ commit }) => {
      fetch('https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/ressources-glossaire.yaml')
        .then((response) => response.text())
        .then((dataYaml) => {
          commit('SET_RESSOURCES_GLOSSAIRE_LIST', { list: processYamlFile(dataYaml) });
        })
        .catch((error) => {
          console.log(error);
          // this.error = error;
        });
    },
    GET_RESSOURCES_GLOSSAIRE_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_RESSOURCES_GLOSSAIRE_LIST', { list: processModelList(ressourcesGlossaireYamlData) });
    },
    GET_RESSOURCES_SOUTIENS_LIST_FROM_LOCAL_YAML: ({ commit, getters }) => {
      const soutiens = processModelList(ressourcesSoutiensYamlData);
      // soutiens: get question_author and/or quiz_tag object
      soutiens.map((s) => {
        const soutienQuizTag = getters.getTagById(s.quiz_tag);
        Object.assign(s, { question_author: s.question_author, quiz_tag: soutienQuizTag });
        return s;
      });
      commit('SET_RESSOURCES_SOUTIENS_LIST', { list: soutiens });
    },
    GET_RESSOURCES_AUTRES_APPS_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_RESSOURCES_AUTRES_APPS_LIST', { list: processModelList(ressourcesAutresAppsYamlData) });
    },
    /**
     * Get stats
     */
    GET_STATS: ({ commit }) => {
      commit('UPDATE_LOADING_STATUS', true);
      commit('UPDATE_ERROR', null);
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/stats`)
        .then((response) => {
          commit('UPDATE_LOADING_STATUS', false);
          commit('UPDATE_ERROR', null);
          return response.json();
        })
        .then((dataJson) => {
          commit('SET_STATS', { object: dataJson });
        })
        .catch((error) => {
          commit('UPDATE_LOADING_STATUS', false);
          commit('UPDATE_ERROR', error);
          console.log(error);
        });
    },
    /**
     * Update question & quiz filters
     */
    UPDATE_QUESTION_FILTERS: ({ commit, state, getters }, filterObject) => {
      const currentQuestionFilters = filterObject || state.questionFilters;
      const questionsDisplayed = getters.getQuestionsByFilter(currentQuestionFilters);
      commit('SET_QUESTION_FILTERS', { object: currentQuestionFilters });
      commit('SET_QUESTIONS_DISPLAYED_LIST', { list: questionsDisplayed });
    },
    UPDATE_QUIZ_FILTERS: ({ commit, state, getters }, filterObject) => {
      const currentQuizFilters = filterObject || state.quizFilters;
      const quizzesDisplayed = getters.getQuizzesByFilter(currentQuizFilters);
      commit('SET_QUIZ_FILTERS', { object: currentQuizFilters });
      commit('SET_QUIZZES_DISPLAYED_LIST', { list: quizzesDisplayed });
    },
  },
  mutations: {
    UPDATE_LOADING_STATUS: (state, value) => {
      state.loading = value;
    },
    UPDATE_ERROR: (state, value) => {
      state.error = value;
    },
    SET_QUESTION_PUBLISHED_LIST: (state, { list }) => {
      state.questions = list;
      state.questionsDisplayed = list;
    },
    SET_QUESTION_PENDING_VALIDATION_LIST: (state, { list }) => {
      state.questionsPendingValidation = list;
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
    SET_RESSOURCES_GLOSSAIRE_LIST: (state, { list }) => {
      state.ressources.glossaire = list;
    },
    SET_RESSOURCES_SOUTIENS_LIST: (state, { list }) => {
      state.ressources.soutiens = list;
    },
    SET_RESSOURCES_AUTRES_APPS_LIST: (state, { list }) => {
      state.ressources.autresApps = list;
    },
    SET_QUESTION_FILTERS: (state, { object }) => {
      state.questionFilters = object;
    },
    SET_QUIZ_FILTERS: (state, { object }) => {
      state.quizFilters = object;
    },
    SET_QUESTIONS_DISPLAYED_LIST: (state, { list }) => {
      state.questionsDisplayed = list;
    },
    SET_QUIZZES_DISPLAYED_LIST: (state, { list }) => {
      state.quizzesDisplayed = list;
    },
    SET_STATS: (state, { object }) => {
      state.stats = object;
    },
  },
  getters: {
    getCategoryById: (state) => (categoryId) => state.categories.find((c) => (c.id === categoryId)),
    getTagById: (state) => (tagId) => state.tags.find((t) => (t.id === tagId)),
    getTagsByIdList: (state) => (tagIdList) => state.tags.filter((t) => tagIdList.includes(t.id)),
    getQuestionById: (state) => (questionId) => state.questions.find((q) => (q.id === questionId)),
    getQuestionsByIdList: (state) => (questionIdList) => state.questions.filter((q) => questionIdList.includes(q.id)),
    getQuestionsByCategoryName: (state) => (categoryName) => state.questions.filter((q) => (q.category.name === categoryName)),
    getQuestionsByTagName: (state) => (tagName) => state.questions.filter((q) => q.tags.map((qt) => qt.name).includes(tagName)),
    getQuestionsByAuthorName: (state) => (authorName) => state.questions.filter((q) => q.author === authorName),
    getQuestionsByFilter: (state) => (filter) => state.questions.filter((q) => (filter.category ? (q.category.name === filter.category) : true))
      .filter((q) => (filter.tag ? q.tags.map((qt) => qt.name).includes(filter.tag) : true))
      .filter((q) => (filter.author ? (q.author === filter.author) : true))
      .filter((q) => (Number.isInteger(filter.difficulty) ? (q.difficulty === filter.difficulty) : true)),
    getCurrentQuestionIndex: (state) => (currentQuestionId) => state.questionsDisplayed.findIndex((q) => q.id === currentQuestionId),
    getNextQuestionByFilter: (state) => (currentQuestionId) => {
      const currentQuestionIndex = currentQuestionId ? state.questionsDisplayed.findIndex((q) => q.id === currentQuestionId) : state.questionsDisplayed[0];
      return state.questionsDisplayed[currentQuestionIndex + 1] ? state.questionsDisplayed[currentQuestionIndex + 1] : state.questionsDisplayed[0];
    },
    getQuizById: (state) => (quizId) => state.quizzes.find((q) => (q.id === quizId)),
    getQuizzesByFilter: (state) => (filter) => state.quizzes.filter((q) => (filter.tag ? q.tags.map((qt) => qt.name).includes(filter.tag) : true)),
  },
});

export default store;
