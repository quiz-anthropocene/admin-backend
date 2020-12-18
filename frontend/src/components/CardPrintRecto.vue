<template>
  <section class="print" :style="cssVars">
    <!-- Question -->
    <div v-if="question" class="card recto">
      <div class="header">
      </div>
      <div>
        <!-- Question text -->
        <div class="row question">
          <div>
            <h3 v-html="$options.filters.abbr(questionTextWithLineBreaks, glossaire)"></h3>
          </div>
        </div>
        <!-- Question answer choices -->
        <div class="row answers">
          <div class="text-align-left">
            <div class="group" v-for="answer_option_letter in answerChoices" :key="answer_option_letter">
              <div class="letter">
                {{answer_option_letter}}
              </div>
              <div class="answer">
                <label v-bind:for="answer_option_letter">&nbsp;{{ question['answer_option_' + answer_option_letter] }}</label>
              </div>
            </div>
          </div>
        </div>
        <!-- Question hint & form submit -->
        <div v-if="question.hint" class="row no-gutters justify-content-center">
          <div class="col-md-10 col-lg-8">
            <div class="alert alert-warning-custom text-align-left margin-bottom-10 padding-10">💡{{ question.hint }}</div>
          </div>
        </div>
      </div>
      <div class="footer row">
        <div class="logo col-md-4">
          <img src="./../assets/logo.png" alt="">

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
export default {
  name: 'CardPrintRexto',
  props: {
    question: Object,
    context: Object,
    bgColor: {
      type: String,
      default: '#00000',
    },
    index: Number,
  },
  components: {
  },
  data() {
    return {
      answerChoices: ['a', 'b', 'c', 'd'],
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
