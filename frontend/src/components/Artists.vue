<template>
  <section class="section">
    <div class="container">
      <b-form-input class="title" v-model="search" @update="searchTyped"
                    placeholder="Artist name"></b-form-input>
      <b-pagination-nav :link-gen="linkGen" :number-of-pages="this.pages" limit="7" first-number
                        last-number align="center" use-router @change="pageClick"
                        class="paginationHome" style="margin-bottom: 0.5em;">
      </b-pagination-nav>
      <div class="columns is-multiline is-mobile" style="margin-top: 0.5em;">
        <div v-for="(artist, index) in filteredArtists" :key="index"
             class="column is-one-fifth-fullhd is-one-quarter-widescreen
           is-one-quarter-desktop is-one-third-tablet is-half-mobile">
          <a :href="'/page/1?artist='+artist" :title="artist">
            <div class="card">
              <header class="card-header" style="padding: inherit !important;"
                      :title="artist">
                <p class="card-header-title">{{ artist }}</p>
              </header>
            </div>
          </a>
        </div>
      </div>
      <b-pagination-nav :link-gen="linkGen" :number-of-pages="this.pages" limit="7" first-number
                        last-number align="center" use-router @change="pageClick"
                        class="paginationHome" style="margin-top: 0.5em;">
      </b-pagination-nav>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Artists',
  data() {
    return {
      qtdPages: 90,
      search: '',
      artists: [],
      filteredArtists: [],
      page: `${this.$route.params.page}`,
      pages: 1,
    };
  },
  methods: {
    getArtists() {
      this.$root.$data.searchBar = '';
      document.title = 'HentaiReader Artists';
      const path = `${this.$globalUrl}/artists`;
      axios.get(path)
        .then((res) => {
          this.artists = res.data.artists;
          this.filteredArtists = this.artists.slice((this.page - 1) * this.qtdPages,
            this.page * this.qtdPages);
          this.pages = Math.ceil(res.data.artists.length / this.qtdPages);
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
    searchTyped() {
      if (this.search.length > 0) {
        this.filteredArtists = this.artists.filter(elem => elem.toLowerCase()
          .indexOf(this.search.toLowerCase()) > -1);
        this.page = 1;
        this.pages = Math.ceil(this.filteredArtists.length / this.qtdPages);
      } else {
        this.filteredArtists = this.artists.slice((this.page - 1) * this.qtdPages,
          this.page * this.qtdPages);
        this.page = 1;
        this.pages = Math.ceil(this.artists.length / this.qtdPages);
      }
    },
    pageClick(page) {
      this.page = page;
      const start = (page - 1) * this.qtdPages;
      const end = page * this.qtdPages;
      this.filteredArtists = this.artists.slice(start, end);
    },
    linkGen(pageNum) {
      return {
        name: 'Artists',
        params: { page: pageNum },
        query: this.$route.query,
      };
    },
  },
  mounted() {
    this.getArtists();
  },
};
</script>

<style scoped>
.paginationHome > li > a {
  color: red;
}
</style>
