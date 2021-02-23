<template>
  <div class="alert alert-primary margin-0" role="alert">
    <div id="fb-root"></div>
    <div class="row">
      <div class="col-md">
        {{ $t('messages.shareQuiz') }}
      </div>
      <div class="col-md">
        <div class="share-buttons row justify-content-center">
          <div class="share-button">
            <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button share-button" data-size="large" :data-text="twitterDataText" data-related="AnthroQuiz" data-show-count="false">Partager sur Twitter</a>
          </div>
          <div class="share-button">
            <!-- Your share button code -->
            <div class="fb-share-button share-button"
              :data-href="quizShareUrl"
              data-layout="button"
              data-size="large"
            >
            </div>
          </div>
          <div class="share-button">
            <button class="linkedin-button" @click="shareLinkedIn">
              <svg viewBox="0 0 24 24" width="20px" height="20px" x="0" y="0" preserveAspectRatio="xMinYMin meet">
                  <g style="fill: currentColor">
                      <rect x="-0.003" style="fill:none;" width="24" height="24"></rect>
                      <path style="" d="M20,2h-16c-1.1,0-2,0.9-2,2v16c0,1.1,0.9,2,2,2h16c1.1,0,2-0.9,2-2V4C22,2.9,21.1,2,20,2zM8,19h-3v-9h3V19zM6.5,8.8C5.5,8.8,4.7,8,4.7,7s0.8-1.8,1.8-1.8S8.3,6,8.3,7S7.5,8.8,6.5,8.8zM19,19h-3v-4c0-1.4-0.6-2-1.5-2c-1.1,0-1.5,0.8-1.5,2.2V19h-3v-9h2.9v1.1c0.5-0.7,1.4-1.3,2.6-1.3c2.3,0,3.5,1.1,3.5,3.7V19z"></path>
                  </g>
              </svg>
              <span>Share</span>
            </button>
          </div>
          <div class="share-button share-button-url">
            <input v-model="quizShareUrl" id="quiz-share-url">
            <!-- Partager le quiz : <strong id="quiz-share-url">{{ quizShareUrl }}</strong> -->
            <a class="fake-link share-button" @click="copyQuizShareUrlToClipboard()">📋&nbsp;{{ textCopy }}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ShareBox',
  data() {
    return {
      textCopy: 'Copier l\'URL',
      textCopied: 'URL copiée',
    };
  },
  props: {
    quiz: String, // Add the component to question later
    quizName: String,
    score: String,
  },
  computed: {
    quizShareUrl() {
      // return window.location.origin + this.$route.path;
      // In order to test in local we need to have a valid url (not localhost)
      return `https://quizanthropocene.fr${this.$route.path}`;
    },
    twitterDataText() {
      // On peut mettre un message plus engageant avec le score réaliser, le titre du quiz, ...
      return `${this.quizName}`;
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
    shareLinkedIn() {
      const url = `https://www.linkedin.com/shareArticle?mini=true&url=${this.quizShareUrl}`;
      window.open(url, '_blank');
    },
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
  margin-top: 10px;
}
.share-button {
  margin-left: 10px;
}
.share-button-url {
  vertical-align: middle;
}
.linkedin-button {
  /* I kept the value from the linkedIn real share button */
  background-color: #0073b1;
  height: 28px;
  padding: 0 10px 0 8px;
  border: none;
  border-radius: 0.3rem;
  color: #fff;
  display: inline-block;
  font-family: -apple-system,system-ui,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Fira Sans,Ubuntu,Oxygen,Oxygen Sans,Cantarell,Droid Sans,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Lucida Grande,Helvetica,Arial,sans-serif!important;
  font-weight: 600;
  overflow: hidden;
  outline-width: 2px;
  position: relative;
  text-align: center;
  text-decoration: none;
  vertical-align: sub;
  white-space: nowrap;
}
.linkedin-button:hover{
  background-color:#006097!important
}
.linkedin-button:focus{
  outline: none;
}
.linkedin-button>span{
  vertical-align: bottom;
  margin-left: 4px;
  font-size: 13px;
}
</style>
