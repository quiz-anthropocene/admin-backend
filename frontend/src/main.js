import Vue from 'vue';

import router from './router';
import store from './store';
import './filters';

import App from './App.vue';
import i18n from './i18n';

Vue.config.productionTip = false;
// Vue.config.performance = true;

/**
 * App
 */
new Vue({
  router,
  store,
  i18n,
  render: (h) => h(App),
}).$mount('#app');
