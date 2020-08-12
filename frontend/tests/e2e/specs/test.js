// For authoring Nightwatch tests, see
// https://nightwatchjs.org/guide

module.exports = {
  // 'default e2e tests': (browser) => {
  //   browser
  //     .init()
  //     .waitForElementVisible('#app')
  //     .assert.elementPresent('.hello')
  //     .assert.containsText('h1', 'Welcome to Your Vue.js App')
  //     .assert.elementCount('img', 1)
  //     .end();
  // },

  // 'example e2e test using a custom command': (browser) => {
  'home page': (browser) => {
    browser
      .openHomepage()
      .assert.elementPresent('header')
      .assert.elementPresent('footer')
      .assert.elementCount('button', 3)
      .useXpath()
      .assert.containsText('(//button)[1]', 'Tous les quiz')
      .assert.containsText('(//button)[2]', 'Toutes les questions')
      .assert.containsText('(//button)[3]', 'Ressources')
      .end();
  },
};
