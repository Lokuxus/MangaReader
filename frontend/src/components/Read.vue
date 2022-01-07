<template>
  <section class="section">
    <div class="container">
      <div class="box" id="box">
        <b-pagination-nav v-if="this.page !== 'all-pages'" :link-gen="linkGen"
                          :number-of-pages="this.pages.length" limit="7" first-number last-number
                          align="center" use-router @change="pageClick"
                          :value="numPage" class="paginationRead" style="margin-bottom: 1em;">
        </b-pagination-nav>
        <div v-if="this.page === 'all-pages' && this.pages.length > 1">
          <figure v-for="apage in pages" class="image" v-bind:key="apage"
                  style="padding-bottom: 1em">
            <img :src="$globalUrl+'/view/page/'+book+'/'+apage">
          </figure>
        </div>
        <a v-else @click="keyPressed('ArrowRight')">
          <figure class="image">
            <img :src="$globalUrl+'/view/page/'+this.book+'/'+this.page">
          </figure>
        </a>

        <b-pagination-nav v-if="this.page !== 'all-pages'" :link-gen="linkGen"
                          :number-of-pages="this.pages.length" limit="7" first-number last-number
                          align="center" use-router @change="pageClick"
                          :value="numPage" class="paginationRead" style="margin-top: 1em;
                           margin-bottom: 1em;">
        </b-pagination-nav>
        <p class="centered">
          <a :href="'/view/'+this.book">« Return to gallery</a>
        </p>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Read',
  data() {
    return {
      book: `${this.$route.params.id}`,
      bookInfo: '',
      page: `${this.$route.params.page}`,
      numPage: 1,
      pages: [1],
    };
  },
  methods: {
    getBookInfo() {
      const path = `${this.$globalUrl}/view/${this.$route.params.id}`;
      axios.get(path)
        .then((res) => {
          this.pages = res.data.pages;
          this.bookInfo = res.data.book_info;
          document.title = this.bookInfo.title;
          if (this.pages.indexOf(this.page) === -1) {
            this.numPage = 1;
          } else {
            this.numPage = this.pages.indexOf(this.page) + 1;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
    pageClick(page) {
      this.numPage = page;
      this.page = this.pages[page - 1];
    },
    linkGen(pageNum) {
      return `/read/${this.book}/${this.pages[pageNum - 1]}`;
    },
    scrollToElement(options) {
      const el = document.getElementById('box');
      if (el) {
        el.scrollIntoView(options);
      }
    },
    keyPressed(key) {
      let pageChanged = false;
      if (key === 'ArrowRight') {
        if (this.numPage < this.pages.length) {
          this.numPage += 1;
          this.page = this.pages[this.numPage - 1];
          pageChanged = true;
        }
      } else if (key === 'ArrowLeft') {
        if (this.numPage > 1) {
          this.numPage -= 1;
          this.page = this.pages[this.numPage - 1];
          pageChanged = true;
        }
      }
      if (pageChanged) {
        this.$router.push(`/read/${this.book}/${this.page}`);
        this.scrollToElement({ behavior: 'smooth' });
      }
    },
  },
  mounted() {
    this.getBookInfo();
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        this.keyPressed(e.key);
      }
    });
  },
};
</script>

<style scoped>
.centered {
  text-align: center;
}
</style>
