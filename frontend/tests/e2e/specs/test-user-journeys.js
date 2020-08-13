module.exports = {
  'user can start a quiz': (browser) => {
    browser
      // home page
      .openHomepage()
      .useXpath()
      .assert.containsText('(//main//button)[1]', 'Tous les quiz')
      .click('(//main//button)[1]')
      .useCss()
      // quiz list page
      .assert.urlContains('quiz')
      .assert.elementPresent('#quiz-list')
      .useXpath()
      .assert.containsText('(//main//a[contains(@class, "card")]//h2)[1]', 'Anéantissement de la biodiversité')
      .click('(//main//a[contains(@class, "card")])[1]')
      .useCss()
      // quiz detail page
      .assert.urlContains('quiz/17')
      .assert.containsText('.card h2', 'Anéantissement de la biodiversité')
      .assert.containsText('div[class*="quiz-start"] button', 'Commencer le quiz')
      .click('div[class*="quiz-start"] button')
      // quiz detail first question page
      .assert.elementPresent('.question')
      .assert.not.elementPresent('.answer')
      .assert.containsText('button[type="submit"]', 'Valider')
      .assert.not.elementPresent('div[class="question-next"] button')
      .end();
  },

  'user can select a random question': (browser) => {
    browser
      // home page
      .openHomepage()
      .useXpath()
      .assert.containsText('(//main//button)[2]', 'Toutes les questions')
      .click('(//main//button)[2]')
      .useCss()
      // question list page
      .assert.urlContains('questions')
      .assert.elementPresent('#question-list')
      .useXpath()
      .assert.elementPresent('(//div[@id="question-list"]//a)[1]')
      .click('(//div[@id="question-list"]//a)[1]')
      .useCss()
      // question detail page
      .assert.elementPresent('.question')
      .assert.not.elementPresent('.answer')
      .assert.elementPresent('.question h2')
      .end();
  },
};
