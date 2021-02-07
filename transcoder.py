import threading, queue
import azure.cognitiveservices.speech as speechsdk
from time import sleep
from config import azure

class Transcoder(object):

    def __init__(self, language='en-EN'):
        self.subscription_key = azure['SUBSCRIPTION_KEY']
        self.region = azure["REGION"]
        self.language = language
        self.buffer = queue.Queue()
        self.closed = True
        print("transcoder constructed")

    def start(self):
        """start streaming"""
        threading.Thread(target=self._process).start()
        print("_process thread started")

    def _process(self):
        """starts azure speech-to-text"""
        speech_config = speechsdk.SpeechConfig(self.subscription_key, self.region)
         # audio_format = speechsdk.audio.AudioInputFormat()
        stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language=self.language)
        
        speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

        print('qsize: {}'.format(self.buffer.qsize()))

        speech_recognizer.start_continuous_recognition()

        try:
            self.closed = False
            while(True):
                frame = next(self._stream_generator())
                if not frame:
                    break
                stream.write(frame)
                sleep(5)
        finally:
            stream.close()
            speech_recognizer.stop_continuous_recognition()
            self.closed = True

    def _stream_generator(self):
        print(self.closed)
        while not self.closed:
            chunk = self.buffer.get()
            print(len(chunk))
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self.buffer.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)


    def write(self, data):
        """writes data to buffer"""
        self.buffer.put(data)
        # print("data written to buffer")


if __name__ == '__main__':
    transcoder = Transcoder()
    transcoder.write(b'{\x03\xff\x00d')
    transcoder.write(b'{\x03\xff\x00d')
    transcoder.closed = False
    print(next(transcoder._stream_generator()))
    