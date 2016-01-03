from draft import app, DEVELOPMENT, PORT, redis

if __name__ == '__main__':
    if DEVELOPMENT:
        redis.flushall()
        app.run(host='0.0.0.0', debug=True, port=PORT)
    else:
        app.run(host='0.0.0.0', port=PORT)
