from draft import app, DEVELOPMENT, PORT, cache

if __name__ == '__main__':
    if DEVELOPMENT:
        cache.flushall()
        app.run(host='0.0.0.0', debug=True, port=PORT)
    else:
        app.run(host='0.0.0.0', port=PORT)
