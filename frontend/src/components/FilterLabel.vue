<template>
  <span class="label" :class="[filterLabelClass, customClass]" @click="$emit('filter-label-clicked', { key: filterType, value: (filterType === 'difficulty') ? filterObject.value : filterObject.name })">
    <!-- name -->
    <span v-if="filterType !== 'difficulty'">{{ filterObject.name }}</span>
    <small v-if="filterType === 'difficulty'"><DifficultyBadge v-bind:difficulty="filterObject.value" /></small>
    <!-- question_count -->
    <small v-if="filterObject.question_count"><i> {{ filterObject.question_count }}</i></small>
  </span>
</template>

<script>
import DifficultyBadge from './DifficultyBadge.vue';

export default {
  name: 'FilterLabel',
  props: {
    filterType: String,
    filterObject: Object,
    customClass: String,
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
