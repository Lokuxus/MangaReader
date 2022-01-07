<template>
  <section class="section">
    <div class="container">
      <div class="box">
        <div class="columns">
          <div class="column is-one-quarter-fullhd is-one-third-desktop is-5-tablet">
            <img :src="$globalUrl+'/cover/' + book.id + '?resize=False'">
          </div>
          <div class="column">
            <h1 class="title">{{ this.book.title }}</h1>
            <table class="view-page-details">
              <tbody>
              <tr>
                <td class="viewcolumn">Artist</td>
                <td>
                  <a :href="'/page/1?artist='+this.book.artist" class="has-text-primary">
                    {{ this.book.artist }}
                  </a>
                </td>
              </tr>
              <tr v-if="this.book.book">
                <td class="viewcolumn">Book</td>
                <td>
                  <a :href="'/page/1?book='+this.book.book" class="has-text-primary">
                    {{ this.book.book }}
                  </a>
                </td>
              </tr>
              <tr v-if="this.book.circle">
                <td class="viewcolumn">Circle</td>
                <td>
                  <a :href="'/page/1?circle='+this.book.circle" class="has-text-primary">
                    {{ this.book.circle }}
                  </a>
                </td>
              </tr>
              <tr v-if="this.book.event">
                <td class="viewcolumn">Event</td>
                <td>
                  <a :href="'/page/1?event='+this.book.event" class="has-text-primary">
                    {{ this.book.event }}
                  </a>
                </td>
              </tr>
              <tr v-if="this.book.language">
                <td class="viewcolumn">Language</td>
                <td>
                  <a :href="'/page/1?language='+this.book.language" class="has-text-primary">
                    {{ this.book.language }}
                  </a>
                </td>
              </tr>
              <tr v-if="this.book.magazine">
                <td class="viewcolumn">Magazine</td>
                <td>
                  <a :href="'/page/1?magazine='+this.book.magazine" class="has-text-primary">
                    {{ this.book.magazine }}
                  </a>
                </td>
              </tr>
              <tr v-if="this.book.parody">
                <td class="viewcolumn">Parody</td>
                <td>
                  <a :href="'/page/1?parody='+this.book.parody" class="has-text-primary">
                    {{ this.book.parody }}
                  </a>
                </td>
              </tr>
              <tr v-if="this.book.publisher">
                <td class="viewcolumn">Publisher</td>
                <td>
                  <a :href="'/page/1?publisher='+this.book.publisher" class="has-text-primary">
                    {{ this.book.publisher }}
                  </a>
                </td>
              </tr>
              <tr>
                <td class="viewcolumn">Pages</td>
                <td>{{ this.book.count }}</td>
              </tr>
              <tr>
                <td class="viewcolumn">Tags</td>
                <td>
                  <span class="tag is-primary"
                        v-for="(tag, index) in this.book.tags"
                        :key="index">
                    <a :href="'/?tag='+tag" v-text="tag" style="color: #FFFFFF"></a>
                  </span>
                </td>
              </tr>
              <tr>
                <td class="viewcolumn">Description</td>
                <td>{{ this.book.description }}</td>
              </tr>
              <tr>
                <td colspan="2">
                  <a :href="'/read/' + book.id + '/all-pages'" class="is-btn">
                    Read Scrollable
                  </a>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div class="container is-hidden-mobile" style="padding-top: 20px;">
      <div class="box">
        <div class="columns is-multiline">
          <div
            class="column is-2-fullhd is-one-fifth-widescreen
            is-one-fifth-desktop is-one-quarter-tablet"
            v-for="(page, index) in this.pages" :key="index">
            <a :href="'/read/' + book.id + '/' + page">
              <div class="card">
                <div class="card-image">
                  <figure class="image">
                    <img :src="$globalUrl+'/view/page/thumb/'+book.id+'/'+page">
                  </figure>
                </div>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'View',
  data() {
    return {
      book: '',
      pages: [],
    };
  },
  methods: {
    getPages() {
      const path = `${this.$globalUrl}/view/${this.$route.params.id}`;
      axios.get(path)
        .then((res) => {
          this.pages = res.data.pages;
          this.book = res.data.book_info;
          document.title = this.book.title;
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
    initForm() {
      this.book = '';
    },
  },
  mounted() {
    this.getPages();
  },
};
</script>

<style scoped>
.tag.is-primary {
  margin-right: 0.5em;
  margin-top: 0.5em;
}

viewcolumn {
  margin-right: 0.75em;
}

.is-btn {
  align-items: center;
  border-radius: 0;
  display: inline-flex;
  font-size: 1.25rem;
  justify-content: center;
  padding-left: 0.75em;
  padding-right: 0.75em;
  white-space: nowrap;
  background-color: #DF691A !important;
  color: #fff !important;
}

</style>
