import os

if __name__ == '__main__':
    os.environ['OPENSHIFT_MONGODB_DB_URL'] = 'mongodb://127.0.0.1:27017'
    from monitor import app
    app.run(debug=True, use_reloader=False, threaded=True)
