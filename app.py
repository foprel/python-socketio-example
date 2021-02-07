import socketio
from transcoder import Transcoder

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})

transcoder = Transcoder()
started = False

# connect event
@sio.event
def connect(sid, environ):
    print(sid, 'connected')

# disconnect event
@sio.event
def disconnect(sid):
    print(sid, 'disconnected')

@sio.event
def write_stream(sid, data):
    print(len(data))
    transcoder.write(data)


@sio.event
def start_stream(sid):
    global started
    if not started:
        transcoder.closed = False
        transcoder.start()
        started = True
    pass