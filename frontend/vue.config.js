/* eslint-disable */

const PrerenderSpaPlugin = require('prerender-spa-plugin');
const path = require('path');

module.exports = {
  // 'default' makes compilation fail in case of errors
  lintOnSave: true,

  indexPath: 'index.vue.html',

  configureWebpack: (config) => {
    if (process.env.NODE_ENV !== 'production') return;
    return {
      plugins: [
        new PrerenderSpaPlugin({
          // Required - The path to the webpack-outputted app to prerender.
          staticDir: path.join(__dirname, 'dist'),

          // Required - Routes to render.
          // If you add routes here, don't forget to edit the public/_redirects file
          routes: [
            '/',
            '/a-propos', '/contribuer', '/glossaire',
            '/quiz/57'
            // '/quiz',
          ],
          postProcess(renderedRoute) {
            if (renderedRoute.originalRoute === '/') {
              renderedRoute.route = '/index';
            }
            renderedRoute.outputPath = path.join(__dirname, 'dist', renderedRoute.route + '.rendered.html');
            return renderedRoute;
          },
        }),
      ],
    };
  },

  pluginOptions: {
    i18n: {
      locale: 'fr',
      fallbackLocale: 'fr',
      localeDir: 'locales',
      enableInSFC: false
    }
  }
};
