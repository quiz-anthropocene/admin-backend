import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    questions: [],
    categories: [],
    tags: [],
    authors: [],
  },
  actions: {
    GET_QUESTION_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions`)
        .then(response => {
          // this.loading = false
          return response.json()
        })
        .then(data => {
          commit('SET_QUESTION_LIST', { list: data })
        })
        .catch(error => {
          console.log(error)
          // this.error = error;
        })
    },
    GET_CATEGORY_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/categories`)
        .then(response => {
          // this.loading = false
          return response.json()
        })
        .then(data => {
          commit('SET_CATEGORY_LIST', { list: data })
        })
        .catch(error => {
          console.log(error)
          // this.error = error;
        })
    },
    GET_TAG_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/tags`)
        .then(response => {
          // this.loading = false
          return response.json()
        })
        .then(data => {
          commit('SET_TAG_LIST', { list: data })
        })
        .catch(error => {
          console.log(error)
          // this.error = error;
        })
    },
    GET_AUTHOR_LIST: ({ commit }) => {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/authors`)
        .then(response => {
          // this.loading = false
          return response.json()
        })
        .then(data => {
          commit('SET_AUTHOR_LIST', { list: data })
        })
        .catch(error => {
          console.log(error)
          // this.error = error;
        })
    },
  },
  mutations: {
    SET_QUESTION_LIST: (state, { list }) => {
      state.questions = list
    },
    SET_CATEGORY_LIST: (state, { list }) => {
      state.categories = list
    },
    SET_TAG_LIST: (state, { list }) => {
      state.tags = list
    },
    SET_AUTHOR_LIST: (state, { list }) => {
      state.authors = list
    }
  },
  getters: {
    getQuestionById: state => questionId => {
      return state.questions.find(q => (q.id === parseInt(questionId)));
    },
    getQuestionsByCategoryName: state => categoryName => {
      return state.questions.filter(q => (q.category === categoryName));
    },
    getQuestionsByTagName: state => tagName => {
      return state.questions.filter(q => q.tags.includes(tagName));
    },
    getQuestionsByAuthorName: state => authorName => {
      return state.questions.filter(q => q.author === authorName);
    },
    getQuestionsByFilter: state => filter => {
      return state.questions.filter(q => (filter.categoryName ? (q.category === filter.categoryName) : true))
                            .filter(q => (filter.tagName ? q.tags.includes(filter.tagName) : true));
    }
  }
})

export default store
