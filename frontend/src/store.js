import Vue from 'vue';
import Vuex from 'vuex';

import constants from './constants';

// webpack + vue-cli-plugin-yaml
import configurationYamlData from '../../data/configuration.yaml';
import statsYamlData from '../../data/stats.yaml';
import authorsYamlData from '../../data/authors.yaml';
import difficultyLevelsYamlData from '../../data/difficulty-levels.yaml';
import categoriesYamlData from '../../data/categories.yaml';
import tagsYamlData from '../../data/tags.yaml';
import questionsYamlData from '../../data/questions.yaml';
import quizzesYamlData from '../../data/quizzes.yaml';
import quizQuestionsYamlData from '../../data/quiz-questions.yaml';
import quizRelationshipsYamlData from '../../data/quiz-relationships.yaml';
import ressourcesGlossaireYamlData from '../../data/ressources-glossaire.yaml';
import ressourcesSoutiensYamlData from '../../data/ressources-soutiens.yaml';
import ressourcesAutresAppsYamlData from '../../data/ressources-autres-apps.yaml';

Vue.use(Vuex);

/**
 * Place to store app-wide variables
 */
const store = new Vuex.Store({
  state: {
    loading: false,
    error: null,
    configuration: {},
    questions: [],
    questionsValidated: [],
    questionsDisplayed: [],
    questionFilters: {
      category: null,
      tag: null,
      author: null,
      difficulty: null,
    },
    questionsPendingValidation: [],
    quizzes: [],
    quizzesPublished: [],
    quizzesDisplayed: [],
    quizFilters: {
      tag: null,
      author: null,
    },
    quizRelationships: [],
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
     * Get app configuration
     */
    GET_CONFIGURATION_DICT_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_CONFIGURATION_DICT', { dict: configurationYamlData[0] });
    },
    /**
     * Get questions
     * Pre-processing ?
     * - keep only validated questions
     * - enrich with categories, tags
     */
    GET_QUESTION_LIST_FROM_LOCAL_YAML: ({ commit, state, getters }) => {
      // questions
      const questions = questionsYamlData;
      // questions: get category & tags objects
      questions.map((q) => {
        const questionCategory = getters.getCategoryById(q.category);
        const questionTags = getters.getTagsByIdList(q.tags);
        Object.assign(q, { category: questionCategory }, { tags: questionTags });
        return q;
      });
      const questionsValidated = questions.filter((el) => el.validation_status === constants.QUESTION_VALIDATION_STATUS_OK);
      commit('SET_QUESTION_LIST', { list: questions });
      commit('SET_QUESTION_VALIDATED_LIST', { list: questionsValidated });

      // update categories: add question_count
      state.categories.forEach((c) => {
        c.question_count = questionsValidated.filter((q) => q.category.name === c.name).length;
      });

      // update tags: add question_count
      state.tags.forEach((t) => {
        t.question_count = questionsValidated.filter((q) => q.tags.map((qt) => qt.id).includes(t.id)).length;
      });
    },
    GET_QUESTION_PENDING_VALIDATION_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      const questionsPendingValidation = questionsYamlData.filter((el) => el.validation_status === constants.QUESTION_VALIDATION_STATUS_IN_PROGRESS);
      commit('SET_QUESTION_PENDING_VALIDATION_LIST', { list: questionsPendingValidation });
    },
    /**
     * Get quizzes
     * Pre-processing ?
     * - keep only published quizs
     * - enrich with questions, tags
     */
    GET_QUIZ_LIST_FROM_LOCAL_YAML: ({ commit, state, getters }) => {
      const quizzes = quizzesYamlData;
      // quiz: get question and tag objects
      quizzes.map((q) => {
        // get quiz questions + order + only get question ids
        const quizQuestionsList = quizQuestionsYamlData.filter((qq) => qq.quiz === q.id);
        quizQuestionsList.sort((a, b) => a.order - b.order);
        const quizQuestionsIdList = quizQuestionsList.map((qq) => qq.question);
        const quizQuestions = getters.getQuestionsByIdList(quizQuestionsIdList);
        // get quiz tags
        const quizTags = getters.getTagsByIdList(q.tags);
        // assign
        Object.assign(q, { questions: quizQuestions }, { tags: quizTags });
        return q;
      });
      const quizzesPublished = quizzes.filter((el) => el.publish === true);
      commit('SET_QUIZ_LIST', { list: quizzes });
      commit('SET_QUIZ_PUBLISHED_LIST', { list: quizzesPublished });

      // update tags: add quiz_count
      state.tags.forEach((t) => {
        t.quiz_count = quizzesPublished.filter((q) => q.tags.map((qt) => qt.id).includes(t.id)).length;
      });
    },
    /**
     * Get quiz relationships
     * Pre-processing ? None
     */
    GET_QUIZ_RELATIONSHIP_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_QUIZ_RELATIONSHIP_LIST', { list: quizRelationshipsYamlData });
    },
    /**
     * Get authors
     * Pre-processing ? None
     */
    GET_AUTHOR_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_AUTHOR_LIST', { list: authorsYamlData });
    },
    /**
     * Get difficulty-levels
     * Pre-processing ? None
     */
    GET_DIFFICULTY_LEVEL_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_DIFFICULTY_LEVEL_LIST', { list: difficultyLevelsYamlData });
    },
    /**
     * Get categories
     * Pre-processing ? None
     */
    GET_CATEGORY_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_CATEGORY_LIST', { list: categoriesYamlData });
    },
    /**
     * Get tags
     * Pre-processing ? None
     */
    GET_TAG_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_TAG_LIST', { list: tagsYamlData });
    },
    /**
     * Get ressources: glossaire, soutiens, autres apps
     * Pre-processing ? for soutiens, append quiz tag or question author
     */
    GET_RESSOURCES_GLOSSAIRE_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_RESSOURCES_GLOSSAIRE_LIST', { list: ressourcesGlossaireYamlData });
    },
    GET_RESSOURCES_SOUTIENS_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_RESSOURCES_SOUTIENS_LIST', { list: ressourcesSoutiensYamlData });
    },
    GET_RESSOURCES_AUTRES_APPS_LIST_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_RESSOURCES_AUTRES_APPS_LIST', { list: ressourcesAutresAppsYamlData });
    },
    /**
     * Get app stats
     */
    GET_STATS_DICT_FROM_LOCAL_YAML: ({ commit }) => {
      commit('SET_STATS_DICT', { dict: statsYamlData });
    },
    /**
     * Update question & quiz filters
     */
    UPDATE_QUESTION_FILTERS: ({ commit, state, getters }, filterObject) => {
      const currentQuestionFilters = filterObject || state.questionFilters;
      const questionsDisplayed = getters.getQuestionsValidatedByFilter(currentQuestionFilters)
        .sort(() => Math.random() - 0.5) // random order
        .sort((a, b) => a.difficulty - b.difficulty); // order by difficulty (easiest to hardest)
      commit('SET_QUESTION_FILTERS', { object: currentQuestionFilters });
      commit('SET_QUESTIONS_DISPLAYED_LIST', { list: questionsDisplayed });
    },
    UPDATE_QUIZ_FILTERS: ({ commit, state, getters }, filterObject) => {
      const currentQuizFilters = filterObject || state.quizFilters;
      const quizzesDisplayed = getters.getQuizzesPublishedByFilter(currentQuizFilters);
      commit('SET_QUESTION_FILTERS', { object: currentQuizFilters });
      // We are not using the quizFilterVairable anymore
      // commit('SET_QUIZ_FILTERS', { object: currentQuizFilters });
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
    SET_CONFIGURATION_DICT: (state, { dict }) => {
      state.configuration = dict;
    },
    SET_QUESTION_LIST: (state, { list }) => {
      state.questions = list;
    },
    SET_QUESTION_VALIDATED_LIST: (state, { list }) => {
      state.questionsValidated = list;
      state.questionsDisplayed = list;
    },
    SET_QUESTION_PENDING_VALIDATION_LIST: (state, { list }) => {
      state.questionsPendingValidation = list;
    },
    SET_QUIZ_LIST: (state, { list }) => {
      state.quizzes = list;
    },
    SET_QUIZ_PUBLISHED_LIST: (state, { list }) => {
      state.quizzesPublished = list;
    },
    SET_QUIZ_RELATIONSHIP_LIST: (state, { list }) => {
      state.quizRelationships = list;
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
    SET_STATS_DICT: (state, { dict }) => {
      state.stats = dict;
    },
  },
  getters: {
    getCategoryById: (state) => (categoryId) => state.categories.find((c) => (c.id === categoryId)),
    getTagById: (state) => (tagId) => state.tags.find((t) => (t.id === tagId)),
    getTagsByIdList: (state) => (tagIdList) => state.tags.filter((t) => tagIdList.includes(t.id)),
    getDifficultyLevelEmojiByValue: (state) => (difficultyLevelValue) => state.difficultyLevels.find((dl) => (dl.value === parseInt(difficultyLevelValue, 10))).emoji,
    // questions
    getQuestionById: (state) => (questionId) => state.questions.find((q) => (q.id === questionId)),
    getQuestionsByIdList: (state) => (questionIdList) => state.questions.filter((q) => questionIdList.includes(q.id)),
    getQuestionsByCategoryName: (state) => (categoryName) => state.questions.filter((q) => (q.category.name === categoryName)),
    getQuestionsByTagName: (state) => (tagName) => state.questions.filter((q) => q.tags.map((qt) => qt.name).includes(tagName)),
    getQuestionsByAuthorName: (state) => (authorName) => state.questions.filter((q) => q.author === authorName),
    getQuestionsValidatedByFilter: (state) => (filter) => state.questionsValidated.filter((q) => (filter.category ? (q.category.name === filter.category) : true))
      .filter((q) => (filter.tag ? q.tags.map((qt) => qt.name).includes(filter.tag) : true))
      .filter((q) => (filter.author ? (q.author === filter.author) : true))
      .filter((q) => (filter.difficulty ? (q.difficulty === parseInt(filter.difficulty, 10)) : true)),
    getCurrentQuestionIndex: (state) => (currentQuestionId) => state.questionsDisplayed.findIndex((q) => q.id === currentQuestionId),
    getNextQuestionByFilter: (state) => (currentQuestionId) => {
      const currentQuestionIndex = currentQuestionId ? state.questionsDisplayed.findIndex((q) => q.id === currentQuestionId) : state.questionsDisplayed[0];
      return state.questionsDisplayed[currentQuestionIndex + 1] ? state.questionsDisplayed[currentQuestionIndex + 1] : state.questionsDisplayed[0];
    },
    // quiz
    getQuizById: (state) => (quizId) => state.quizzes.find((q) => (q.id === quizId)),
    getQuizzesPublishedByFilter: (state) => (filter) => state.quizzesPublished.filter((q) => (filter.tag ? q.tags.map((qt) => qt.name).includes(filter.tag) : true))
      .filter((q) => (filter.author ? (q.author === filter.author) : true)),
    getQuizRelationshipsById: (state) => (quizId) => state.quizRelationships.filter((qr) => (qr.from_quiz === quizId) || (qr.to_quiz === quizId)),
  },
});

export default store;
