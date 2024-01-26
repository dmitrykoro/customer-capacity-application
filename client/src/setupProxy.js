const { createProxyMiddleware } = require('http-proxy-middleware');

const apiProxy = createProxyMiddleware(
    [
        '/login',
        '/customer/checkin',
        '/customer/checkout',
        '/logout',
        '/facility',
        '/manage-facilities/full',
        '/manage-facilities/delete',
        '/manage-facilities/filter'
    ], {
        target: 'http://127.0.0.1:4999',
        changeOrigin: true
    }
);

module.exports = function(app) {
    app.use(apiProxy);
};
