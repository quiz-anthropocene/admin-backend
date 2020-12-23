<template>
  <section>
    <button class="print-btn" @click="print">Print</button>
    <div id="cardslist" ref='printMe' class="printbg">
      <div
        class="page"
        v-for="(page, index) in questionByPages"
        :key="'page-'+ index"
        :id="'page-' + index">
        <div
          class="row line"
          :style="getPosition(index)"
          v-for="(question, index) in page" :key="question.id">
          <CardPrint :question="question" />
        </div>
      </div>
    </div>
    <!-- OUTPUT -->
    <!-- <div id="imageCards">

    </div> -->
    <!-- <img :src="output"> -->
  </section>
</template>

<script>
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
      return this.$store.state.questionsValidated.slice(0, 100);
    },
    questionByPages() {
      const chunk = 3;
      let i;
      let j;
      const array = [];
      for (i = 0, j = this.questions.length; i < j; i += chunk) {
        const temparray = this.questions.slice(i, i + chunk);
        array.push(temparray);
      }
      return array;
    },
  },
  methods: {
    getPosition(index) {
      return `top:${(index + 1) * 100}px;`;
    },
    clickPrint() {
      this.print();
    },
    async print() {
      const g = document.createElement('div');
      g.setAttribute('id', 'print');
      // await this.generateAllImages();
      this.$htmlToPaper('cardslist');
    },
    async generateAllImages() {
      // const options = {
      //   backgroundColor: null,
      //   // windowWidth: document.body.scrollWidth,
      //   // windowHeight: document.body.scrollHeight,
      //   // width: 300,
      //   // height: 4 * 100,
      // };
      // for (let i = 0; i < this.questionByPages.length; i++) {
      //   await html2canvas(document.getElementById(`page-${i}`), options).then((canvas) => {
      //     var dataURL = canvas.toDataURL();
      //     console.log(dataURL);
      //     const img = document.createElement("img");
      //     img.setAttribute('src', dataURL);
      //     var element = document.getElementById("imageCards");
      //     element.appendChild(img);
      //   });
      // }
    },
  },

};
</script>
<style scoped lang="scss"  src="../assets/scss/print.scss">
img {
  z-index: 4;
}
</style>
