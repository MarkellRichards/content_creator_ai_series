const url_config = {
    CONTENT_SERVER_URL: process.env.PUBLIC_CONTENT_SERVER,
    CONTENT_SERVER_WS: process.env.PUBLIC_WEBSOCKET_CONTENT_SERVER
}

const config = {
    ...url_config
}

export default config