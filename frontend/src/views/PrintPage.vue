<template>
  <section>
    <button class="print-btn" @click="print">Print</button>
    <div id="cardslist" ref='printMe' class="printbg">
      <div
        class="row line"
        :style="getPosition(index)"
        v-for="(question, index) in questions" :key="question.id">
        <CardPrint :question="question" />
      </div>
    </div>
    <!-- OUTPUT -->
    <img :src="output">
  </section>
</template>

<script>
import html2canvas from 'html2canvas';
import { metaTagsGenerator } from '../utils';
import CardPrint from '../components/CardPrint.vue';

export default {
  name: 'Print',
  components: {
    CardPrint,
  },
  metaInfo() {
    const title = '404';
    return {
      meta: metaTagsGenerator(title),
    };
  },
  data() {
    return {
      output: null,
    };
  },
  computed: {
    questions() {
      return this.$store.state.questionsValidated.slice(0, 4);
    },
  },
  methods: {
    getPosition(index) {
      return `top:${(index + 1) * 100}px;`;
    },
    clickPrint() {
      this.print();
    },
    print() {
      const options = {
        backgroundColor: null,
        // windowWidth: document.body.scrollWidth,
        // windowHeight: document.body.scrollHeight,
        // width: 300,
        // height: 4 * 100,
      };
      console.log(document.getElementById('cardslist'));
      console.log(options);
      html2canvas(document.getElementById('cardslist'), options).then((canvas) => {
        console.log(canvas);
        document.body.appendChild(canvas);
        const img = canvas.toDataURL();
        window.open(img);
      });
    },
  },

};
</script>
<style scoped lang="scss">
.line {
  display: flex;
  flex-flow: row wrap;
  margin: auto;
}
.print-btn {
  // position: fixed;
  z-index: 2;
}
.printbg {
  z-index: 1;
  background-color: #fff;
}
img {
  z-index: 4;
}
</style>
