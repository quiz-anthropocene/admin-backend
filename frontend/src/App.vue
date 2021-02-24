<template>
  <div id="app">
    <Header />
    <section>
      <div v-show="loading" class="alert alert-primary" role="alert">Chargement...</div>
      <div v-if="error" class="alert alert-danger" role="alert">
        Erreur de connexion 🤔
        <a href="#" @click="initData()">Réessayer</a>
        <button type="button" class="close" data-dismiss="alert" aria-label="Close" @click="dismissAlert()">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
    </section>
    <main class="container-md">
      <router-view></router-view>
    </main>
    <Footer />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

export default {
  name: 'App',
  metaInfo: {
    // title: 'Quiz de l\'Anthropocène',
    titleTemplate: (titleChunk) => {
      return titleChunk ? `${titleChunk} | Quiz de l'Anthropocène` : 'Quiz de l\'Anthropocène';
    },
    meta: [
      {
        property: 'description',
        vmid: 'description',
        template: (chunk) => {
          return chunk || 'Des questions/réponses pour mieux appréhender les limites de notre planète';
        },
      },
      {
        property: 'og:url',
        vmid: 'og:url',
        template: (chunk) => {
          return chunk ? `https://quizanthropocene.fr${chunk}` : 'https://quizanthropocene.fr';
        },
      },
      {
        property: 'og:title',
        vmid: 'og:title',
        // content: 'Quiz de l\'Anthropocène',
        template: (chunk) => {
          return chunk ? `${chunk} | Quiz de l'Anthropocène` : 'Quiz de l\'Anthropocène';
        },
      },
      {
        property: 'og:description',
        vmid: 'og:description',
        template: (chunk) => {
          return chunk || 'Des questions/réponses pour mieux appréhender les limites de notre planète';
        },
      },
      {
        property: 'og:image',
        vmid: 'og:image',
        template: (chunk) => {
          return chunk || `${process.env.VUE_APP_DOMAIN_URL}/summary_large_image.png`;
        },
      },
      {
        property: 'twitter:url',
        vmid: 'twitter:url',
        template: (chunk) => {
          return chunk ? `https://quizanthropocene.fr${chunk}` : 'https://quizanthropocene.fr';
        },
      },
      {
        property: 'twitter:title',
        vmid: 'twitter:title',
        // content: 'Quiz de l\'Anthropocène',
        template: (chunk) => {
          return chunk ? `${chunk} | Quiz de l'Anthropocène` : 'Quiz de l\'Anthropocène';
        },
      },
      {
        property: 'twitter:description',
        vmid: 'twitter:description',
        template: (chunk) => {
          return chunk || 'Des questions/réponses pour mieux appréhender les limites de notre planète';
        },
      },
      {
        property: 'twitter:image',
        vmid: 'twitter:image',
        template: (chunk) => {
          return chunk || `${process.env.VUE_APP_DOMAIN_URL}/summary_large_image.png`;
        },
      },
    ],

  },
  components: {
    Header,
    Footer,
  },

  computed: {
    loading() {
      return this.$store.state.loading;
    },
    error() {
      return this.$store.state.error;
    },
  },

  watch: {
    // eslint-disable-next-line
    '$i18n.locale' (newLocale, oldLocale) {
      // reload data (includes updating locale in the store)
      this.initData();
    },
  },

  mounted() {
    // set locale
    if (Object.keys(this.$route.query).length) {
      if (Object.keys(this.$route.query).includes('locale')) {
        this.$i18n.locale = this.$route.query.locale || process.env.VUE_APP_I18N_LOCALE;
      }
    }
    // load data
    this.initData();
  },

  methods: {
    initData() {
      this.$store.dispatch('SET_LOCALE');
      this.$store.dispatch('GET_CONFIGURATION_DICT_FROM_LOCAL_YAML');
      this.$store.dispatch('GET_DIFFICULTY_LEVEL_LIST_FROM_LOCAL_YAML');
      this.$store.dispatch('GET_AUTHOR_LIST_FROM_LOCAL_YAML');
      this.$store.dispatch('GET_CATEGORY_LIST_FROM_LOCAL_YAML');
      this.$store.dispatch('GET_TAG_LIST_FROM_LOCAL_YAML');
      this.$store.dispatch('GET_QUESTION_LIST_FROM_LOCAL_YAML');
      this.$store.dispatch('GET_QUIZ_LIST_FROM_LOCAL_YAML');
      this.$store.dispatch('UPDATE_QUIZ_FILTERS', {});
      // needed for both glossary page & abbr filter
      this.$store.dispatch('GET_RESSOURCES_GLOSSAIRE_LIST_FROM_LOCAL_YAML');
    },
    dismissAlert() {
      this.$store.dispatch('RESET_LOADING_STATUS');
    },
  },
};
</script>

<style lang="scss">

/* Override bootstrap.min.css */

$theme-colors: (
  "primary": #08519C,
  "secondary": #F33F3F,
  "warning":#f0ad4e // #ffc107
);
$primary-color--active: #7dcaff;
$category-color: var(--secondary);
$category-color-active: #f88787; // last Monochromatic Color
$tag-color: #f3993f;
$tag-color-active: #f8bf87; // last Monochromatic Color
$author-color: #f33f99;
$author-color-active: #f887bf; // last Monochromatic Color
$difficulty-color: #ffd700; // 'gold'
$difficulty-color-active: #ffe34d; // last Monochromatic Color

@import "../node_modules/bootstrap/scss/bootstrap";

html {
  background-color: #F8F8F8;
}
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #F8F8F8;
  text-align: center;
}

h1, h2, h3, h4, h5, h6, p {
  margin-top: 10px;
  margin-bottom: 10px;
}
h1 {
  font-size: 2em;
  font-weight: 700;
}
h2 {
  font-size: 1.5em;
  font-weight: 700;
}
h3 {
  font-size: 1.17em;
  font-weight: 700;
}
h4 {
  font-size: 1em;
  font-weight: 700;
}

button {
  margin: 0;
}

label {
  display: inline; // solves failing &nbsp;
}
form .form-group {
  margin-bottom: 10px; // changing label to inline removes it's margin-bottom of 8px...
}

audio {
  vertical-align: middle;
}

.card-img-top {
  height: 10vw;
  object-fit: cover;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}
.card-body {
  padding: 10px;

  .card-title {
    margin-top: 0;
    margin-bottom: 0;
  }
  .card-subtitle {
    margin-top: 0;
    max-height: 200px;
    overflow-y: scroll;
  }

  button {
    margin-top: 0 !important;
  }
}
.card-footer {
  background-color: inherit; // avoir grey on grey
}

/* Global css */

/* adds a 'opens in new tab' icon. but not for images */
a[target="_blank"]::after {
  content: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAQElEQVR42qXKwQkAIAxDUUdxtO6/RBQkQZvSi8I/pL4BoGw/XPkh4XigPmsUgh0626AjRsgxHTkUThsG2T/sIlzdTsp52kSS1wAAAABJRU5ErkJggg==);
  margin: 0 3px 0 5px;
}
a[href$=".jpg"]::after, a[href$=".jpeg"]::after, a[href$=".png"]::after, a[href$=".svg"]::after,
a.no-after::after {
  display: none;
}

a.no-decoration {
  color: inherit;
  text-decoration: inherit;
}
.fake-link {
  cursor: pointer;
  color: #005995 !important;
}
.fake-link:hover {
  color: #002b49 !important;
  text-decoration: underline !important;
}
.cursor-pointer {
  cursor: pointer;
}

/* show abbr on small screens */
abbr[title]:hover::after,
abbr[title]:focus::after {
  content: " (" attr(title) ")";
}

.margin-0 {
  margin: 0;
}
.margin-5 {
  margin: 5px;
}
.margin-10 {
  margin: 10px;
}
.margin-top-bottom-10 {
  margin-top: 10px;
  margin-bottom: 10px;
}
.margin-left-right-5 {
  margin-left: 5px;
  margin-right: 5px;
}
.margin-left-right-10 {
  margin-left: 10px;
  margin-right: 10px;
}
.margin-left-20 {
  margin-left: 20px;
}
.margin-bottom-0 {
  margin-bottom: 0;
}
.margin-bottom-10 {
  margin-bottom: 10px;
}
.margin-bottom-1em {
  margin-bottom: 1em;
}
.padding-10 {
  padding: 10px;
}
.padding-top-bottom-15 {
  padding-top: 15px;
  padding-bottom: 15px;
}
.padding-top-10 {
  padding-top: 10px;
}
.padding-bottom-5 {
  padding-bottom: 5px;
}
.padding-bottom-10 {
  padding-bottom: 10px;
}
.padding-left-right-0 {
  padding-left: 0;
  padding-right: 0;
}
.padding-left-right-10 {
  padding-left: 10px;
  padding-right: 10px;
}

.height-200 {
  height: 200px;
}
.height-150 {
  height: 150px;
}
.height-50 {
  height: 50px;
}
.max-height-300 {
  max-height: 300px;
  overflow-y: hidden;
}

.color-green {
  color: green;
}
.color-red {
  color: red;
}
.color-tag {
  color: $tag-color;
}

.background-color-dark-grey {
  background-color: #ebebeb;
}

.text-underline-primary {
  text-decoration: underline;
  text-decoration-color: var(--primary);
}
.text-underline-secondary {
  text-decoration: underline;
  text-decoration-color: var(--secondary);
}
.text-underline-tag {
  text-decoration: underline;
  text-decoration-color: $tag-color;
}

.text-align-left {
  text-align: left;
}
.text-align-right {
  text-align: right;
}

h2.special-title {
  text-align: left;
  margin-bottom: 5px;
  color: var(--primary);
}

span.no-wrap {
  white-space: nowrap;
}

.small {
  font-size: small;
}
.smaller {
  font-size: smaller;
}

.btn-primary-light {
  color: #fff;
  background-color: rgba(0, 89, 149, 0.03); // var(--primary);
}

.help-text {
  font-size: smaller;
  font-style: italic;
}

/* Elements */

.label {
  display: inline-block;
  border: 1px solid;
  border-radius: 15px;
  margin: 2.5px;
  padding: 2.5px 5px;
}
.label--active {
  background-color: $primary-color--active;
  text-shadow: 0px 0px 1px black;
}
.label-hidden {
  border: 1px transparent;
  padding: 2.5px;
  // cursor: auto;
}
.label-category {
  border-color: $category-color;
}
.label-category--active {
  background-color: $category-color-active;
  text-shadow: 0px 0px 1px black;
}
.label-tag {
  border-color: $tag-color;
}
.label-tag--active {
  background-color: $tag-color-active;
  text-shadow: 0px 0px 1px black;
}
.label-author {
  border-color: $author-color;
}
.label-author--active {
  background-color: $author-color-active;
  text-shadow: 0px 0px 1px black;
}
.label-difficulty {
  border-color: $difficulty-color;
}
.label-difficulty--active {
  background-color: $difficulty-color-active;
  text-shadow: 0px 0px 1px black;
}

hr.custom-separator {
  border: 0 none;
  // height: 1px;
  width: 50%;
  color: var(--primary);
  background-color: var(--primary);
}

.separator-with-text {
  display: flex;
  align-items: center;
  text-align: center;
}
.separator-with-text::before,
.separator-with-text::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--primary);
}
.separator-with-text::before {
  margin-right: 0.5em;
}
.separator-with-text::after {
  margin-left: 0.5em;
}

/* Media */

@media(hover: hover) and (pointer: fine) {
  .label-category--with-hover:hover {
    background-color: $category-color-active;
    cursor: pointer;
  }
  .label-tag--with-hover:hover {
    background-color: $tag-color-active;
    cursor: pointer;
  }
  .label-author--with-hover:hover {
    background-color: $author-color-active;
    cursor: pointer;
  }
  .label-difficulty--with-hover:hover {
    background-color: $difficulty-color-active;
    cursor: pointer;
  }
}
</style>
