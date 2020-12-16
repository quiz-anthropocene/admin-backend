<template>
  <div class="flex">
    <CardPrintRecto :question="question" bg-color="#FED106" :index="question.id"/>
    <CardPrintVerso :question="question" bg-color="#FED106" :index="question.id"/>
  </div>
</template>

<script>
import CardPrintRecto from './CardPrintRecto.vue';
import CardPrintVerso from './CardPrintVerso.vue';

export default {
  name: 'CardPrint',
  props: {
    question: Object,
  },
  components: {
    CardPrintRecto,
    CardPrintVerso,
  },

  data() {
    return {
    };
  },

  computed: {
  },
};
</script>
<style scoped lang="scss">
.flex {
  display: flex;
  flex-flow: row wrap;
}
</style>
