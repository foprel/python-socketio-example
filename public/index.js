const sio = io();

// connect event
sio.on("connect", () => {
    console.log("connected");
    sio.emit("sum", {"numbers": [1, 2]}, (result) =>{
        console.log(result);
    });
    sio.on('mult', (data, cb) => {
        result = data.numbers[0] * data.numbers[1]
        cb(result)
    });
});

// diconnect event
sio.on("disconnect", () => {
    console.log("disconnected");
});