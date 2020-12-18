import Vue from 'vue';
import VueHtmlToPaper from 'vue-html-to-paper';

import router from './router';
import store from './store';
import './filters';

import App from './App.vue';

const basePath = process.env.VUE_APP_DOMAIN_URL;

const options = {
  name: '_blank',
  specs: ['fullscreen=yes', 'titlebar=yes', 'scrollbars=yes'],
  styles: [
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
    `${basePath}/print.css`,
  ],
};

Vue.use(VueHtmlToPaper, options);
Vue.config.productionTip = false;
// Vue.config.performance = true;

/**
 * App
 */
new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
