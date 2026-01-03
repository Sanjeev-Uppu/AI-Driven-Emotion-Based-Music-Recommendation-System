const video = document.getElementById("video");
const audio = document.getElementById("player");
const emotionText = document.getElementById("emotion");

const startBtn = document.getElementById("startBtn");
const detectBtn = document.getElementById("detectBtn");

let stream = null;

startBtn.onclick = async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        detectBtn.disabled = false;
    } catch {
        alert("Camera access denied!");
    }
};

detectBtn.onclick = async () => {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    const imageData = canvas.toDataURL("image/jpeg");

    try {
        const res = await fetch("http://127.0.0.1:5000/detect", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ frame: imageData })
        });

        const data = await res.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        emotionText.innerText = "Detected Emotion: " + data.emotion;

        audio.pause();
        audio.src = data.song_url;
        audio.load();
        audio.play();

    } catch (e) {
        alert("Backend not responding");
    }
};
