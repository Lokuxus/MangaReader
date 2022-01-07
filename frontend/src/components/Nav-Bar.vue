<template>
  <div class="navbar is-primary"
       style="background-color: #DF691A !important;
        padding: 0 0 0 0 !important;">
    <b-navbar class="navbar is-primary"
              style="background-color: inherit !important; padding: unset !important;"
              toggleable="lg" type="dark" variant="info">
      <div class="navbar-brand" style="padding: unset !important;">
        <b-navbar-brand class="navbar-item" style="font-size: 1.5em !important;" href="/">
          MangaReader
        </b-navbar-brand>
      </div>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <div class="navbar-menu has-text-light">
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav class="ml-auto">
            <b-nav-form v-on:submit.prevent="" style="padding-top: 0.9em; !important;">
              <b-input size="sm" class="mr-sm-2" v-model="$root.$data.searchBar"
                       placeholder="Search Name, Artist or Tag"
                       v-on:keydown.enter="submit"></b-input>
              <b-button size="sm" class="my-2 my-sm-0" v-on:click="submit">Search
              </b-button>
            </b-nav-form>
          </b-navbar-nav>
        </b-collapse>
      </div>
    </b-navbar>
  </div>
</template>

<script>

export default {
  name: 'Nav-Bar',
  data() {
    return {
      searchData: '',
    };
  },
  methods: {
    submit() {
      this.$router.push(`/page/1?query=${this.$root.$data.searchBar}`);
      this.$router.go();
    },
  },
};
</script>

<style scoped>

</style>
