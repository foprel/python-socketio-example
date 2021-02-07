const startRecording = document.getElementById("start");
const stopRecording = document.getElementById("stop")
const sio = io();

const config = {
    audio: {
        autoGainControl: '',
        channelCount: '',
        echoCancellation: '',
        latency: '',
        noiseSuppression: '',
        sampleRate: '',
        sampleSize: '',
        volume: ''
    }
};

// connect event
sio.on("connect", () => {
    console.log("connected");
    startRecording.disabled = false;
});

startRecording.onclick = () => {
    startRecording.disabled = true;
    navigator.getUserMedia(config, (stream) => {
        const recorder = new MediaRecorder(stream);
            recorder.ondataavailable = (event) => {
                console.log(event.data);
        };
        recorder.start(1000);
        console.log("recording started");
    
        stopRecording.disabled = false;

        stopRecording.onclick = () => {
            // stop MediaRecorder instance
            recorder.stop();
            // stop all tracks in getUserMedia stream 
            stream.getTracks().forEach(track => {
                track.stop();
            })
            startRecording.disabled = false;
            stopRecording.disabled = true;
            console.log("recording stopped")
        };

    }, (error) => {
        console.error(JOSN.stringify(error));
    });
};

// diconnect event
sio.on("disconnect", () => {
    console.log("disconnected");
});