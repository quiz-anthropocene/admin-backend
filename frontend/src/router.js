import Vue from 'vue'
import VueRouter from 'vue-router'

import HomePage from './views/HomePage.vue'
import QuestionListPage from './views/QuestionListPage.vue'
import QuestionDetailPage from './views/QuestionDetailPage.vue'
import CategoryListPage from './views/CategoryListPage.vue'
import CategoryDetailPage from './views/CategoryDetailPage.vue'
import AboutPage from './views/AboutPage.vue'
import StatsPage from './views/StatsPage.vue'
import ContributePage from './views/ContributePage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/', name: 'home', component: HomePage
  },
  {
    path: '/questions', name: 'question-list', component: QuestionListPage,
    meta: {
      title: "Know Your Planet - Questions"
    }
  },
  {
    path: '/questions/:questionId', name: 'question-detail', component: QuestionDetailPage,
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
    path: '/a-propos', name: 'about', component: AboutPage,
    meta: {
      title: "Know Your Planet - A propos"
    }
  },
  {
    path: '/stats', name: 'stats', component: StatsPage,
    meta: {
      title: "Know Your Planet - Statistiques"
    }
  },
  {
    path: '/contribuer', name: 'contribute', component: ContributePage,
    meta: {
      title: "Know Your Planet - Contribuer"
    }
  }
]

export const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  console.log(to, from);
  if (to.meta.title) {
    if (to.params.questionId) {
      document.title = to.meta.title + (to.params.questionId ? `#${to.params.questionId}` : '');
    } else if (to.params.categoryKey) {
      document.title = to.meta.title + (to.params.categoryKey ? `#${to.params.categoryKey}` : '');
    }
  } else {
    document.title = 'Know Your Planet';
  }
  next();
});
