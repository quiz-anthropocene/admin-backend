module.exports = {
  'user can start a quiz': (browser) => {
    browser
      // home page
      .openHomepage()
      .useXpath()
      .assert.containsText('//main/section/div[2]/div/a/button', 'Tous les quiz')
      .click('//main/section/div[2]/div/a/button')
      .useCss()
      // quiz list page
      .assert.urlContains('quiz')
      .assert.elementPresent('#quiz-list')
      .useXpath()
      .assert.elementPresent('(//main//a[contains(@class, "card")]//h2)[1]')
      .click('(//main//a[contains(@class, "card")])[1]')
      .useCss()
      // quiz detail page
      // .assert.urlContains('quiz/17')
      .assert.elementPresent('.card h2')
      .assert.containsText('button[id="quiz-start-btn"]', 'Commencer le quiz')
      .click('button[id="quiz-start-btn"]')
      // quiz detail first question page
      .assert.elementPresent('.question')
      .assert.not.elementPresent('.answer')
      .assert.containsText('button[type="submit"]', 'Valider')
      .assert.not.elementPresent('button[id="question-next-btn"]')
      .end();
  },

  // 'user can select a random question and answer it': (browser) => {
  //   browser
  //     // home page
  //     .openHomepage()
  //     .useXpath()
  //     .assert.containsText('(//main//button)[2]', 'Toutes les questions')
  //     .click('(//main//button)[2]')
  //     .useCss()
  //     // question list page
  //     .assert.urlContains('questions')
  //     .assert.elementPresent('#question-list')
  //     .useXpath()
  //     .assert.elementPresent('(//div[@id="question-list"]//a)[1]')
  //     .click('(//div[@id="question-list"]//a)[1]')
  //     .useCss()
  //     // question detail page
  //     .assert.elementPresent('.question')
  //     .assert.not.elementPresent('.answer')
  //     .assert.elementPresent('.question h2')
  //     .assert.containsText('button[id="question-next-btn"]', 'Question suivante')
  //     // question detail page : answer question
  //     .answerQuestion()
  //     // .waitForElementVisible('div[class*="answer"]')
  //     .assert.elementPresent('.answer')
  //     .assert.elementPresent('section[class*="feedback-card"]')
  //     .assert.containsText('button[id="question-next-btn"]', 'Question suivante')
  //     .end();
  // },
};
