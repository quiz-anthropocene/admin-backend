module.exports = {
  async command(url = '') {
    // Other Nightwatch commands are available via "this"
    this.url(this.launch_url + url);
    this.waitForElementVisible('#app');
  },
};
