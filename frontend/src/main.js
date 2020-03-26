import Vue from 'vue'
import VueRouter from 'vue-router'

import App from './App.vue'
import QuestionList from './components/QuestionList.vue'
import QuestionDetail from './components/QuestionDetail.vue'
import CategoryListPage from './components/CategoryListPage.vue'
import CategoryDetailPage from './components/CategoryDetailPage.vue'
import About from './components/About.vue'
import Stats from './components/Stats.vue'

Vue.use(VueRouter)
Vue.config.productionTip = false

const routes = [
  {
    path: '/', name: 'home', component: QuestionList
  },
  {
    path: '/questions', name: 'question-list', component: QuestionList
  },
  {
    path: '/questions/:questionId', name: 'question-detail', component: QuestionDetail,
    meta: {
      title: "Know Your Planet - Question "
    }
  },
  {
    path: '/categories', name: 'category-list', component: CategoryListPage,
    meta: {
      title: "Know Your Planet - Catégories"
    }
  },
  {
    path: '/categories/:categoryKey', name: 'category-detail', component: CategoryDetailPage,
    meta: {
      title: "Know Your Planet - Catégorie "
    }
  },
  {
    path: '/a-propos', name: 'about', component: About,
    meta: {
      title: "Know Your Planet - A propos"
    }
  },
  {
    path: '/stats', name: 'stats', component: Stats,
    meta: {
      title: "Know Your Planet - Statistiques"
    }
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  const questionId = to.params.questionId;
  if (to.meta.title) {
    document.title = to.meta.title + (questionId ? `#${questionId}` : '');
  } else {
    document.title = 'Know Your Planet';
  }
  next();
});

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
