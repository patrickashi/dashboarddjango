module.exports = function override(config, env) {
    // Modify the devServer configuration
    if (env === 'development') {
        config.devServer = {
            ...config.devServer,
            allowedHosts: [
                'localhost',
                '127.0.0.1'
            ],
        };
    }
    return config;
};
