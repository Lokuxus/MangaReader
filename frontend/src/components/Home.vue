<template>
  <section class="section">
    <div class="container">
      <b-pagination-nav :link-gen="linkGen" :number-of-pages="this.pages" limit="7" first-number
                        last-number align="center" use-router @change="pageClick"
                        class="paginationHome" style="margin-bottom: 0.5em;">
      </b-pagination-nav>
      <div class="columns is-multiline is-mobile" style="margin-top: 0.5em;">
        <div v-for="(book, index) in books" :key="index"
             class="column is-one-fifth-fullhd is-one-quarter-widescreen
           is-one-quarter-desktop is-one-third-tablet is-half-mobile">
          <a :href="'/view/'+book.bookid" :title="book.title">
            <div class="card">
              <header class="card-header" style="padding: inherit !important;" :title="book.title">
                <p class="card-header-title">{{ book.title }}</p>
              </header>
              <div class="card-image">
                <b-card-img :src="$globalUrl+'/cover/' + book.bookid + '?resize=True'"></b-card-img>
              </div>
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
  name: 'Home',
  data() {
    return {
      books: [],
      page: `${this.$route.params.page}`,
      pages: 1,
    };
  },
  methods: {
    getBooks() {
      let params = '';
      let title = 'HentaiReader';
      this.$root.$data.searchBar = '';
      Object.keys(this.$route.query)
        .forEach((key) => {
          params += `&${key}=${this.$route.query[key]}`;
          if (key === 'query') {
            this.$root.$data.searchBar = `${this.$route.query[key]}${this.$root.$data.searchBar}`;
          }
          title += ` ${this.$route.query[key]}`;
        });
      document.title = title;
      // console.log(this.$globalUrl);
      const path = `${this.$globalUrl}/books?page=${this.page}${params}`;
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
          this.pages = res.data.pages > 0 ? res.data.pages : 1;
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
    pageClick(page) {
      this.page = page;
      this.books = [];
      this.getBooks();
    },
    linkGen(pageNum) {
      return {
        name: 'Home',
        params: { page: pageNum },
        query: this.$route.query,
      };
    },
  },
  mounted() {
    this.getBooks();
  },
};
</script>

<style scoped>
.paginationHome > li > a {
  color: red;
}
</style>
