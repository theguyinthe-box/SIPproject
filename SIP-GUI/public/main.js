let imageFilename = "";

window.onload = async function () {
    timer_element = document.getElementById("countdown");
    // Set source to a 1x1 transparent GIF
    document.getElementById("rand_img").src = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs%3D';
    await waitForNextSelection(timeBetweenSelections);
    await getRandomImage();
    startSelectionCountdown();
}

let selection_interval = null;
let selection_delta = 1;
let timePerImage = 10; //seconds
async function startSelectionCountdown(){
    selectionTimer = Date.now()
    let timeLeft = timePerImage;
    if (selection_interval) clearInterval(selection_interval);
    selection_interval = setInterval(() => {
        timeLeft -= 1.0 * selection_delta;
        if (timeLeft <= 0) { //We want the user to see the zero first before moving on
            //console.log("Time's up!");
            clearInterval(selection_interval);
            makeSelection("No Response");
        }
    }, 1000 * selection_delta);
}


let timer_element = null;
let timeBetweenSelections = 3; //seconds
let tickRate = 500; //milliseconds 
let wait_interval = null;
let waiting_delta = .05;
async function waitForNextSelection(s) {
    let buttons = document.querySelectorAll('.button');
    buttons.forEach(btn => btn.classList.add('waiting'));    
    timer_element.innerText = Math.ceil(s);
    timer_element.style.opacity = 1; // Show the timer when waiting

    if (wait_interval) clearInterval(wait_interval);
    let timeLeft = s;


    return new Promise((resolve) => { wait_interval = setInterval(() => {
            timeLeft -= 1.0 * waiting_delta; // Normalize the time decrement to be consistent with the tick rate
            timer_element.innerText = Math.ceil(timeLeft);
            
            if (timeLeft <= 0) { //We want the user to see the zero first before moving on
                //console.log("Time to make next selection!");
                clearInterval(wait_interval);
                wait_interval = null;
                resolve();
                timer_element.style.opacity = 0; // Hide the timer when not waiting
                buttons.forEach(btn => btn.classList.remove('waiting'));
            }
        }, tickRate * waiting_delta);
    });
}

let selectionTimer = Date.now();
async function makeSelection(userSelection, timeTaken) {
    if (wait_interval){ //Don't allow user to make selection if they are supposed to be waiting for next image
        console.log("User tried to make selection while waiting for next image. Ignoring selection.");
        return;
    }

    clearInterval(selection_interval);
    // Set source to a 1x1 transparent GIF
    document.getElementById("rand_img").src = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs%3D';
    try {
        const response = await fetch('http://127.0.0.1:3001/userInput', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                selection: userSelection,
                filename: imageFilename,
                timeTaken: (Date.now() - selectionTimer)
            })
        });
        await waitForNextSelection(timeBetweenSelections);
        await getRandomImage();
        startSelectionCountdown();
        return response;
    } catch (error) {
        console.error('Error:', error);
        alert("Error sending request: " + error);
    }
}

let currURL = "";
async function getRandomImage() {
    const baseUrl = 'http://127.0.0.1:3001/randomImage';
    const timestamp = new Date().getTime();
    const uniqueUrl = `${baseUrl}?t=${timestamp}`;
    try {
        const response = await fetch(uniqueUrl, {
            method: "GET",
        });
        response.status === 404 && (() => { window.location.href = "complete.html" })();
        imageFilename = response.headers.get('X-Image-Filename');
        const blob = await response.blob();
        if(currURL) { window.URL.revokeObjectURL(currURL); } // Clean up previous URL to avoid memory leaks

        currURL = window.URL.createObjectURL(blob);
        document.getElementById("rand_img").src = currURL;
        
        return response;
    } catch (error) {
        console.error('Error:', error);
        alert("Error sending request: " + error);
    }
}

const delay = (durationMs) => {return new Promise(resolve => setTimeout(resolve, durationMs));}
async function waitForServer(timeout=2000) {
    const url = 'http://127.0.0.1:3001/getStatus';
    while (!(await checkServerStatus())) {
        await delay(timeout);
    }
    return true; 
}

async function waitForServerDown(timeout=2000) {
    const url = 'http://127.0.0.1:3001/getStatus';
    while (await checkServerStatus()) {
        await delay(timeout);
    }
    return true; 
}

async function checkServerStatus(){
    const url = 'http://127.0.0.1:3001/getStatus';
    try {
        const response = await fetch(url);
        if (response.ok) { return true; }
    } catch (error) {}
    return false
}