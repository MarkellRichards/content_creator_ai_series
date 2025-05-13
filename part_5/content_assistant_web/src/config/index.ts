const url_config = {
  CONTENT_SERVER_URL: process.env.PUBLIC_CONTENT_SERVER + '/content',
  CONTENT_SERVER_WS: process.env.PUBLIC_WEBSOCKET_CONTENT_SERVER + '/content',
};

const config = {
  ...url_config,
};

export default config;
