<template>
  <div id="app">
    <nav-bar></nav-bar>
    <router-view/>
  </div>
</template>
<style>
#app {
  background-color: #1f2d3b;
}

</style>
<script>
// eslint-disable-next-line import/extensions
import NavBar from '@/components/Nav-Bar';

export default {
  components: { NavBar },
};
</script>
