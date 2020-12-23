import Vue from 'vue';
import VueRouter from 'vue-router';
import VueMeta from 'vue-meta';

import HomePage from './views/HomePage.vue';
import QuestionPage from './views/QuestionPage.vue';
import QuestionListPage from './views/QuestionListPage.vue';
import QuestionDetailPage from './views/QuestionDetailPage.vue';
import QuizPage from './views/QuizPage.vue';
import QuizListPage from './views/QuizListPage.vue';
import QuizDetailPage from './views/QuizDetailPage.vue';
import AboutPage from './views/AboutPage.vue';
import RessourcesPage from './views/RessourcesPage.vue';
import StatsPage from './views/StatsPage.vue';
import GlossaryPage from './views/GlossaryPage.vue';
import ContributePage from './views/ContributePage.vue';
import NotFoundPage from './views/NotFoundPage.vue';
import PrintPage from './views/PrintPage.vue';

Vue.use(VueRouter);
Vue.use(VueMeta);

const routes = [
  {
    path: '/', name: 'home', component: HomePage,
  },
  {
    path: '/questions',
    component: QuestionPage,
    children: [
      {
        path: '',
        name: 'question-list',
        component: QuestionListPage,
      },
      {
        path: ':questionId',
        name: 'question-detail',
        component: QuestionDetailPage,
      },
    ],
  },
  {
    path: '/quiz',
    component: QuizPage,
    children: [
      {
        path: '',
        name: 'quiz-list',
        component: QuizListPage,
      },
      {
        path: ':quizId',
        name: 'quiz-detail',
        component: QuizDetailPage,
      },
    ],
  },
  {
    path: '/a-propos',
    name: 'about',
    component: AboutPage,
  },
  {
    path: '/print',
    name: 'print',
    component: PrintPage,
  },
  {
    path: '/ressources',
    name: 'ressources',
    component: RessourcesPage,
    meta: {
      title: 'Quiz de l\'Anthropocène - Ressources',
    },
  },
  {
    path: '/stats',
    name: 'stats',
    component: StatsPage,
  },
  {
    path: '/glossaire',
    name: 'glossary',
    component: GlossaryPage,
  },
  {
    path: '/contribuer',
    name: 'contribute',
    component: ContributePage,
  },
  {
    // will match everything
    path: '*',
    name: '404',
    component: NotFoundPage,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
  // eslint-disable-next-line
  scrollBehavior (to, from, savedPosition) {
    if (to.hash) {
      return { selector: to.hash };
    }
    return { x: 0, y: 0 };
  },
});

export default router;
