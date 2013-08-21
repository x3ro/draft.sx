from gistio import app, HEROKU, PORT, cache

if __name__ == '__main__':
    if HEROKU:
        app.run(host='0.0.0.0', port=PORT)
    else:
        cache.flushall()
        app.run(host='0.0.0.0', debug=True, port=PORT)
