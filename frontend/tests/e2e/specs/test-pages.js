// For authoring Nightwatch tests, see
// https://nightwatchjs.org/guide

module.exports = {
  // '@disabled': true,
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
      .assert.elementCount('button', 6)
      .useXpath()
      .assert.containsText('//main/section/div[2]/div/a/button', 'Tous les quiz')
      // .assert.containsText('(//main//button)[2]', 'Toutes les questions')
      .assert.containsText('//main/section/div[5]/div/a/button', 'Ressources')
      .assert.containsText('//main/section/div[6]/div/form/div[2]/button', 'Je m\'inscris !')
      .useCss()
      .end();
  },

  'about page': (browser) => {
    browser
      .openUrl('a-propos/')
      .assert.elementPresent('header')
      .assert.elementPresent('footer')
      .useXpath()
      .assert.containsText('(//main//h3)[1]', 'Pourquoi cette application')
      .useCss()
      .end();
  },

  'ressources page': (browser) => {
    browser
      .openUrl('ressources/')
      .assert.elementPresent('header')
      .assert.elementPresent('footer')
      .useXpath()
      .assert.containsText('(//main//h3)[1]', 'Les associations et les personnes qui participent de près ou de loin au projet')
      .useCss()
      .assert.elementPresent('#ressources-soutiens-list')
      .end();
  },

  // 'quiz list page': (browser) => {
  //   browser
  //     .openUrl('quiz/')
  //     .assert.elementPresent('header')
  //     .assert.elementPresent('footer')
  //     .assert.elementPresent('.filter-box')
  //     .assert.elementPresent('#quiz-list')
  //     .end();
  // },

  'quiz detail page': (browser) => {
    browser
      .openUrl('quiz/1/')
      .assert.elementPresent('header')
      .assert.elementPresent('footer')
      .assert.elementPresent('.card h2')
      .assert.containsText('div[class*="quiz-start"] button', 'Commencer le quiz')
      .end();
  },

  'question list page': (browser) => {
    browser
      .openUrl('questions/')
      .assert.elementPresent('header')
      .assert.elementPresent('footer')
      .assert.elementPresent('.filter-box')
      .assert.elementPresent('#question-list')
      .end();
  },

  'question detail page': (browser) => {
    browser
      .openUrl('questions/1/')
      .assert.elementPresent('header')
      .assert.elementPresent('footer')
      .assert.elementPresent('.question')
      .assert.not.elementPresent('.answer')
      .assert.elementPresent('.question h2')
      .assert.elementPresent('.question h3')
      .assert.containsText('button[type="submit"]', 'Valider')
      .assert.containsText('div[class*="question-next"] button', 'Question suivante')
      .end();
  },
};
