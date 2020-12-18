<template>
  <section class="print" :style="cssVars">
    <!-- Question -->
    <div v-if="question" class="card verso">
      <div class="header">
      </div>
      <div>
        <!-- Question text -->
        <div class="row good-answer">
          Réponse
          <div class="letter">
            {{ question["answer_correct"] }}
          </div>
          <!-- <div class="ans">
            {{ question["answer_option_" + question["answer_correct"]] }}
          </div> -->
        </div>
        <!-- Question answer choices -->
        <div class="row answer-explanation">
          <div class="no-gutters text-align-left">
            <div class="col-sm-auto">
              <p title="Explication">
                <span>ℹ️&nbsp;</span>
                <span v-html="$options.filters.abbr(questionAnswerExplanationWithLineBreaks, glossaire)"></span>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="footer row">
        <div class="logo col-md-4">
          <vue-qrcode :value="questionUrl" />
          <!-- <img src="../assets/qrcode.png" alt=""> -->
        </div>
        <div class="col-md-8 content">
          <div class="title">
            Quiz anthropocène
          </div>
          <div class="category">
            {{ question.category.name }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import VueQrcode from 'vue-qrcode';

export default {
  name: 'CardPrintVerso',
  props: {
    question: Object,
    context: Object,
    bgColor: {
      type: String,
      default: '#000000',
    },
    index: Number,
  },
  components: {
    VueQrcode,
  },
  data() {
    return {
      answerChoices: ['a', 'b', 'c', 'd'],
      dimension: {
        width: 62,
        height: 88,
      },
    };
  },

  computed: {
    glossaire() {
      return this.$store.state.ressources.glossaire;
    },
    questionTextWithLineBreaks() {
      return this.question.text.replace(/(?:\r\n|\r|\n)/g, '<br />');
    },
    questionAnswerExplanationWithLineBreaks() {
      return this.question.answer_explanation.replace(/(?:\r\n|\r|\n)/g, '<br />');
    },
    questionUrl() {
      return `${process.env.VUE_APP_DOMAIN_URL}/questions/${this.question.id}`;
    },
    cssVars() {
      return {
        '--bg-color': this.bgColor,
      };
    },
  },

  watch: {
  },

  mounted() {
  },

  methods: {
  },
};
</script>

<style lang="scss" scoped src="../assets/scss/print.scss">
</style>
