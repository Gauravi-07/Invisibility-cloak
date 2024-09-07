document.addEventListener("DOMContentLoaded", function() {
    const startButton = document.getElementById("start-camera");
    const stopButton = document.getElementById("stop-camera");
    const statusMessage = document.getElementById("status");
    const videoFeed = document.getElementById("video-feed");

    let isCameraActive = false;

    startButton.addEventListener("click", function() {
        if (isCameraActive) return;

        statusMessage.textContent = "Please move out of the frame";
        setTimeout(() => {
            fetch("/start_camera")
                .then(response => response.text())
                .then(data => {
                    if (data === "Camera started") {
                        statusMessage.textContent = "Camera is active";
                        videoFeed.src = "/video_feed";
                        videoFeed.style.display = "block";
                        isCameraActive = true;
                    }
                });
        }, 2000); // Delay to show the "move out of the frame" message
    });

    stopButton.addEventListener("click", function() {
        if (!isCameraActive) return;

        fetch("/stop_camera")
            .then(response => response.text())
            .then(data => {
                if (data === "Camera stopped") {
                    statusMessage.textContent = "Camera stopped";
                    videoFeed.style.display = "none";
                    videoFeed.src = ""; // Stop video feed
                    isCameraActive = false;
                }
            });
    });
});
