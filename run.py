from app import app, socketio, mqtt


if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        use_reloader=True,
        debug=True
    )