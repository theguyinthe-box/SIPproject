let imageFilename = "";

window.onload = function () {
    getRandomImage();
    startSelectionCountdown();
}

let interval = null;
let delta = 1;
let timePerImage = 10; //seconds
async function startSelectionCountdown(){
    let timeLeft = timePerImage;
    if (interval) clearInterval(interval);
    interval = setInterval(() => {
        timeLeft -= 1.0 * delta;

        if (timeLeft > 0) { //We want the user to see the zero first before moving on
        } else {
            console.log("Time's up!");
            clearInterval(interval);
            makeSelection("No Response");
        }
    }, 1000 * delta);
}

async function makeSelection(userSelection) {
    try {
        const response = await fetch('http://localhost/userInput', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                selection: userSelection,
                filename: imageFilename
            })
        });
        await getRandomImage();
        startSelectionCountdown();
        return response;
    } catch (error) {
        console.error('Error:', error);
        alert("Error sending request: " + error);
    }
    
}

async function getRandomImage() {
    const baseUrl = 'http://localhost/randomImage';
    const timestamp = new Date().getTime();
    const uniqueUrl = `${baseUrl}?t=${timestamp}`;
    try {
        const response = await fetch(uniqueUrl, {
            method: "GET",
        });
        response.status === 404 && (() => { window.location.href = "/complete.html" })();
        imageFilename = response.headers.get('X-Image-Filename');
        const blob = await response.blob();
        document.getElementById("rand_img").src = window.URL.createObjectURL(blob);
        
        return response;
    } catch (error) {
        console.error('Error:', error);
        alert("Error sending request: " + error);
    }
}
