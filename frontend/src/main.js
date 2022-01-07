import 'bootstrap/dist/css/bootstrap.css';
import './assets/css/bulmaswatch.min.css';
import BootstrapVue from 'bootstrap-vue';// Import Bootstrap here
import './assets/css/view.css';
// import './assets/css/view.css';
import Vue from 'vue';
import App from './App.vue';
import router from './router';

Vue.use(BootstrapVue); // Use Bootstrap here
Vue.config.productionTip = false;
Vue.prototype.$globalUrl = `http://${window.location.hostname}:8080/api`;

new Vue({
  router,
  data() {
    return {
      searchBar: '',
    };
  },
  render: h => h(App),
}).$mount('#app');
