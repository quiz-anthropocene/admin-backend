import Vue from 'vue';

/**
 * Common Filters
 * https://gist.github.com/belsrc/672b75d1f89a9a5c192c
 */

Vue.filter('round', (value = 0, decimals = 0) => Math.round(value * (10 ** decimals)) / (10 ** decimals));

Vue.filter('abbr', (value, glossary) => {
  let textEnrichedWithAbbr = value;

  if (glossary) {
    // loop on glossary terms
    glossary.forEach((glossaryItem) => {
      // replace terms
      // TODO: check that it is the full word instead of a subword ?
      textEnrichedWithAbbr = textEnrichedWithAbbr.replace(glossaryItem.name, `<abbr title="${glossaryItem.definition_short}">${glossaryItem.name}</abbr>`);
    });
  }

  return textEnrichedWithAbbr;
});
