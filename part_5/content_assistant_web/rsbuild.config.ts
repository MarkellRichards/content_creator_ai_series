import { TanStackRouterRspack } from '@tanstack/router-plugin/rspack';
import { pluginReact } from '@rsbuild/plugin-react';
import path from 'path';

const isProduction = process.env.NODE_ENV === 'production';

const config = {
  plugins: [pluginReact()],
  entry: 'src/index.tsx',
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['postcss-loader'],
        type: 'css',
      },
    ],
  },
  tools: {
    htmlPlugin: {
      template: './public/index.html',
      filename: 'index.html',
      publicPath: isProduction ? '/content' : '/',
    },
    rspack: {
      plugins: [
        TanStackRouterRspack({ target: 'react', autoCodeSplitting: false }),
      ],
    },
  },
  output: {
    distPath: {
      root: path.resolve(__dirname, 'dist/content'),
    },

    path: path.resolve(__dirname, 'dist/content'),
    clean: true,
    filename: '[name].[contenthash].bundle.js',
    publicPath: isProduction ? '/content/' : '/',
  },
};

module.exports = config;
