import Vue from 'vue';

import router from './router';
import store from './store';
import './filters';

import App from './App.vue';

Vue.config.productionTip = false;

/**
 * App
 */
new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
