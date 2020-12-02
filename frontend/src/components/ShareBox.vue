<template>
  <div class="alert alert-primary margin-0" role="alert">
    <div id="fb-root"></div>
    Vous souhaitez partager le quiz avec vos amis ?
    <div class="share-buttons row justify-content-center">
      <div class="share-button">
        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button share-button" data-size="large" :data-text="twitterDataText" data-related="AnthroQuiz" data-show-count="false">Partager sur Twitter</a>
      </div>
      <div class="share-button">
        <!-- Your share button code -->
        <div class="fb-share-button share-button"
          :data-href="'https://quizanthropocene.fr' + $route.path"
          data-layout="button"
          data-size="large"
        >
        </div>
      </div>
      <div class="share-button share-button-url">
        <input v-model="quizShareUrl" id="quiz-share-url">
        <!-- Partager le quiz : <strong id="quiz-share-url">{{ quizShareUrl }}</strong> -->
        <a class="fake-link share-button" @click="copyQuizShareUrlToClipboard()">📋&nbsp;{{ textCopy }}</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuizDetailPage',
  data() {
    return {
      textCopy: 'Copier l\'URL',
      textCopied: 'URL copiée',
    };
  },
  computed: {
    quizShareUrl() {
      return window.location.origin + this.$route.path;
    },
    twitterDataText() {
      return 'Quiz Anthropocène';
      // return `${this.quiz.questions.filter((q) => q.success).length} / ${this.quiz.questions.length} au #QuizAnthoprocene ${this.quiz.name}.`;
    },
  },

  methods: {
    copyQuizShareUrlToClipboard() {
      const copyText = document.getElementById('quiz-share-url');
      copyText.select();
      const oldValue = this.textCopy;
      this.textCopy = this.textCopied;
      document.execCommand('copy');
      setTimeout(() => {
        this.textCopy = oldValue;
      }, 2000);
    },
  },
  mounted() {
    // Add Twitter script
    const twitterScript = document.createElement('script');
    twitterScript.setAttribute('src', 'https://platform.twitter.com/widgets.js');
    twitterScript.setAttribute('charset', 'utf-8');
    document.head.appendChild(twitterScript);

    // Add Facebook Script
    const fbScript = document.createElement('script');
    fbScript.text = `(function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s); js.id = id;
        js.src = "https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v3.0";
        fjs.parentNode.insertBefore(js, fjs);
      }(document, 'script', 'facebook-jssdk'));`;
    document.body.appendChild(fbScript);

    // data-href="{{ quizShareUrl }}"
  },
};
</script>
<style scoped>

#quiz-share-url {
  /* display: none; */
  background: transparent;
  border: none;
  position: fixed;
  left: -1000px;
}
input:focus{
  outline: none;
}

.share-buttons {
  margin-left: 20px;
  margin-top: 10px;
}
.share-button {
  margin-left: 10px;
}
.share-button-url {
  vertical-align: middle;
}

</style>
