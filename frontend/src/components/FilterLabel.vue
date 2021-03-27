<template>
  <span class="label" :class="[filterLabelClass, customClass]" @click="$emit('filter-label-clicked', { key: filterType, value: filterValue })">
    <!-- cross prefix -->
    <span v-if="showCross">✘&nbsp;</span>
    <!-- name -->
    <span v-if="filterType !== 'difficulty'">{{ filterValue }}</span>
    <small v-if="filterType === 'difficulty'"><DifficultyBadge v-bind:difficulty="filterValue" /></small>
    <!-- question_count or quiz_count -->
    <small v-if="filterCount"><i> {{ filterCount }}</i></small>
  </span>
</template>

<script>
import DifficultyBadge from './DifficultyBadge.vue';

export default {
  name: 'FilterLabel',
  props: {
    filterType: String,
    filterValue: [String, Number],
    filterCount: Number,
    customClass: String,
    showCross: Boolean,
  },
  components: {
    DifficultyBadge,
  },

  computed: {
    filterLabelClass() {
      if (this.filterType === 'category') {
        return 'label-category label-category--with-hover';
      }
      if (this.filterType === 'tag') {
        return 'label-tag label-tag--with-hover';
      }
      if (this.filterType === 'author') {
        return 'label-author label-author--with-hover';
      }
      if (this.filterType === 'difficulty') {
        return 'label-difficulty label-difficulty--with-hover';
      }
      return '';
    },
  },
};
</script>
