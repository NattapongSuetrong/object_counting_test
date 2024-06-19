async function system(status) {
    await fetch(`http://localhost:8888/status/${status}`, {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            if (status === 'ON') {
                alert('System started successfully');
            } else if (status === 'OFF') {
                alert('System stopped successfully');
            }
        } else {
            if (status === 'ON') {
                alert('Failed to start system');
            } else if (status === 'OFF') {
                alert('Failed to stop system');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (status === 'ON') {
            alert('Failed to start system');
        } else if (status === 'OFF') {
            alert('Failed to stop system');
        }
    });
}

async function initCount() {
    // แสดง video container
    document.getElementById("video-container").style.display = "block";
    // ตั้ง src ของ img เป็น API video
    document.getElementById("video-stream").src = getVideo();
}

async function getVideo() {
    await fetch(`http://localhost:8888/video`, {
        method: 'GET'
    })
}