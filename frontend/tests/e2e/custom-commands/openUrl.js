module.exports = {
  async command(url) {
    // Other Nightwatch commands are available via "this"
    // .init() simply calls .url() command with the value of the "launch_url" setting
    this.url(this.launch_url + url);
    this.waitForElementVisible('#app');

    // const result = await this.elements('css selector', '#app ul');
    // this.assert.strictEqual(result.value.length, 3);
  },
};
