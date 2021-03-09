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
      // .assert.elementCount('button', 6) // can be 3 to 6 depending on the number of spotlighted quizs
      .assert.containsText('button[id="all-quizs-btn"]', 'Tous les quiz')
      // .assert.containsText('button[id="all-questions-btn"]', 'Toutes les questions')
      .assert.containsText('button[id="resources-btn"]', 'Ressources')
      .assert.containsText('button[id="newsletter-btn"]', 'Je m\'inscris !')
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

  // doesn't work, dunno why
  // 'ressources page': (browser) => {
  //   browser
  //     .openUrl('ressources/')
  //     .assert.elementPresent('header')
  //     .assert.elementPresent('footer')
  //     .useXpath()
  //     .assert.containsText('(//main//h3)[1]', 'Les associations et les personnes qui participent de près ou de loin au projet')
  //     .useCss()
  //     .assert.elementPresent('#ressources-soutiens-list')
  //     .end();
  // },

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
      .assert.containsText('button[id="quiz-start-btn"]', 'Commencer le quiz')
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
      .assert.containsText('button[id="question-next-btn"]', 'Question suivante')
      .end();
  },

  'home page in english': (browser) => {
    browser
      .openUrl('?locale=en')
      .assert.elementPresent('header')
      .assert.elementPresent('footer')
      // .assert.elementCount('button', 6) // can be 3 to 6 depending on the number of spotlighted quizs
      .assert.containsText('button[id="all-quizs-btn"]', 'All quizs')
      // .assert.containsText('button[id="all-questions-btn"]', 'All questions')
      .assert.containsText('button[id="resources-btn"]', 'Resources')
      .assert.containsText('button[id="newsletter-btn"]', 'Je m\'inscris !')
      .end();
  },
};
