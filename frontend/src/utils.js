/* eslint-disable import/prefer-default-export */

/**
 * Usage: in components, to overwrite default set in App.vue
 */
function metaTagsGenerator(title, description = null, imageUrl = null) {
  const metaTags = [];
  if (title) {
    const titleMetaTags = [
      { property: 'og:title', vmid: 'og:title', content: title },
      { property: 'twitter:title', vmid: 'twitter:title', content: title },
    ];
    metaTags.push(...titleMetaTags);
  }
  if (description) {
    const descriptionMetaTags = [
      { name: 'description', vmid: 'description', content: description },
      { name: 'og:description', vmid: 'og:description', content: description },
      { name: 'twitter:description', vmid: 'twitter:description', content: description },
    ];
    metaTags.push(...descriptionMetaTags);
  }
  if (imageUrl) {
    const imageMetaTags = [
      { property: 'og:image', vmid: 'og:image', content: imageUrl },
      { property: 'twitter:image', vmid: 'twitter:image', content: imageUrl },
    ];
    metaTags.push(...imageMetaTags);
  }
  // if (url) {
  //   { name: 'og:url', vmid: 'og:url', content: url },
  //   { name: 'twitter:url', vmid: 'twitter:url', content: url },
  // }
  return metaTags;
}

export {
  metaTagsGenerator,
};
