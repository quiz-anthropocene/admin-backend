module.exports = {
  async command(answerNumber = 1) {
    // Other Nightwatch commands are available via "this"
    this.useXpath();
    this.click(`(//input[@type="radio"])[${answerNumber}]`);
    this.useCss();
    this.click('button[type="submit"]');
  },
};
