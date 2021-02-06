import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})

# backgound task
# call combines emit and callback
def task(sid):
    sio.sleep(5)
    result = sio.call('mult', {'numbers': [3, 4]}, to=sid)
    print(result)

# connect event
@sio.event
def connect(sid, environ):
    print(sid, 'connected')
    sio.start_background_task(task, sid)

# disconnect event
@sio.event
def disconnect(sid):
    print(sid, 'disconnected')

# message event
@sio.event
def sum(sid, data):
    result = data['numbers'][0] + data['numbers'][1]
    return result