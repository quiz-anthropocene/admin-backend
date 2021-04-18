<template>
  <span class="label" :class="[getFilterLabelClass, customClass]" @click="$emit('filter-label-clicked', { key: filterType, value: filterValue })">
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
    withHover: {
      type: Boolean,
      default: true,
    },
    showCross: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    DifficultyBadge,
  },

  computed: {
    getFilterLabelClass() {
      let filterLabelClass = '';
      if (this.filterType === 'category') {
        filterLabelClass = 'label-category';
      }
      if (this.filterType === 'tag') {
        filterLabelClass = 'label-tag';
      }
      if (this.filterType === 'author') {
        filterLabelClass = 'label-author';
      }
      if (this.filterType === 'difficulty') {
        filterLabelClass = 'label-difficulty';
      }
      if (this.filterType === 'language') {
        filterLabelClass = 'label-language';
      }
      if (this.withHover) {
        // example : 'label-language' --> 'label-language label-language--with-hover'
        filterLabelClass += ` ${filterLabelClass}--with-hover`;
      }
      return filterLabelClass;
    },
  },
};
</script>
