import Vue from 'vue'
import VueRouter from 'vue-router'

import HomePage from './views/HomePage.vue'
import QuestionPage from './views/QuestionPage.vue'
import QuestionListPage from './views/QuestionListPage.vue'
import QuestionDetailPage from './views/QuestionDetailPage.vue'
import CategoryListPage from './views/CategoryListPage.vue'
import CategoryDetailPage from './views/CategoryDetailPage.vue'
import TagListPage from './views/TagListPage.vue'
import TagDetailPage from './views/TagDetailPage.vue'
import AuthorListPage from './views/AuthorListPage.vue'
import AuthorDetailPage from './views/AuthorDetailPage.vue'
import QuizListPage from './views/QuizListPage.vue'
import QuizDetailPage from './views/QuizDetailPage.vue'
import AboutPage from './views/AboutPage.vue'
import StatsPage from './views/StatsPage.vue'
import ContributePage from './views/ContributePage.vue'
import NotFoundPage from './views/NotFoundPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/', name: 'home', component: HomePage
  },
  {
    path: '/questions', component: QuestionPage,
    children: [
      {
        path: '', name: 'question-list', component: QuestionListPage,
        meta: {
          title: "Know Your Planet - Questions"
        }
      },
      {
        path: ':questionId', name: 'question-detail', component: QuestionDetailPage,
        meta: {
          title: "Know Your Planet - Question "
        }
      }
    ]
  },
  {
    path: '/categories', name: 'category-list', component: CategoryListPage,
    meta: {
      title: "Know Your Planet - Catégories"
    }
  },
  {
    path: '/categories/:categoryName', name: 'category-detail', component: CategoryDetailPage,
    meta: {
      title: "Know Your Planet - Catégorie "
    }
  },
  {
    path: '/tags', name: 'tag-list', component: TagListPage,
    meta: {
      title: "Know Your Planet - Tags"
    }
  },
  {
    path: '/tags/:tagName', name: 'tag-detail', component: TagDetailPage,
    meta: {
      title: "Know Your Planet - Tag "
    }
  },
  {
    path: '/auteurs', name: 'author-list', component: AuthorListPage,
    meta: {
      title: "Know Your Planet - Auteurs"
    }
  },
  {
    path: '/auteurs/:authorName', name: 'author-detail', component: AuthorDetailPage,
    meta: {
      title: "Know Your Planet - Auteur "
    }
  },
  {
    path: '/quiz', name: 'quiz-list', component: QuizListPage,
    meta: {
      title: "Know Your Planet - Les Quiz"
    }
  },
  {
    path: '/quiz/:quizId', name: 'quiz-detail', component: QuizDetailPage,
    meta: {
      title: "Know Your Planet - Quiz "
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
  },
  {
    // will match everything
    path: '*', name: '404', component: NotFoundPage,
    meta: {
      title: "Know Your Planet - 404"
    }
  }
]

export const router = new VueRouter({
  routes
})

/**
 * Update the page's title dynamically
 */
router.beforeEach((to, from, next) => {
  // console.log(to, from);
  if (to.meta.title) {
    if (to.params.questionId) {
      document.title = to.meta.title + (to.params.questionId ? `#${to.params.questionId}` : '');
    } else if (to.params.quizId) {
      document.title = to.meta.title + (to.params.quizId ? `#${to.params.quizId}` : '');
    } else if (to.params.categoryName) {
      document.title = to.meta.title + (to.params.categoryName ? `#${to.params.categoryName}` : '');
    } else if (to.params.tagName) {
      document.title = to.meta.title + (to.params.tagName ? `#${to.params.tagName}` : '');
    }
  } else {
    document.title = 'Know Your Planet';
  }
  next();
});
