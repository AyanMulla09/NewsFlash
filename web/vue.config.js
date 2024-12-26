const { defineConfig } = require('@vue/cli-service')
const path = require('path');

function resolve(dir) {
  return path.join(__dirname, dir);
}

module.exports = defineConfig({
  transpileDependencies: true,
  runtimeCompiler: true,
  productionSourceMap: false,
  publicPath: './',
  chainWebpack: (config) => {
    config.resolve.alias
      .set('@', path.resolve(__dirname, 'src'))
    config.resolve.extensions
      .add('.js')
      .add('.vue') 
      .add('.json');

    // pug
    config.module.rule('pug')
      .test(/\.pug$/)
      .use('pug-html-loader')
      .loader('pug-html-loader')
      .end();

    // config Babel
    config.module
      .rule('compile')
      .test(/\.js$/)
      .include
      .end()
      .use('babel')
      .loader('babel-loader')
      .options({
        presets: [
          ['@babel/preset-env', { modules: false }],
        ],
      });

    // config entry file
    config.entry = ['core-js/stable', 'regenerator-runtime/runtime', './src/main.js'];
  },
  devServer: {
    port: 8080, // set port number
    open: true, // Automatically open the browser when starting the project
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // FastAPI address
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      },
    },
  },
});
