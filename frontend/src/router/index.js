import Vue from 'vue';
import Router from 'vue-router';
import Home from '../components/Home.vue';
import View from '../components/View.vue';
import Read from '../components/Read.vue';
import Artists from '../components/Artists.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      redirect: '/page/1',
    },
    {
      path: '/page/:page',
      name: 'Home',
      alias: ['/:page'],
      component: Home,
    },
    {
      path: '/view/:id',
      name: 'View',
      component: View,
    },
    {
      path: '/read/:id/:page',
      name: 'Read',
      component: Read,
    },
    {
      path: '/artists/:page',
      name: 'Artists',
      component: Artists,
    },
  ],
});
