let imageFilename = "";

window.onload = function () {
    getRandomImage();
}


// document.addEventListener('keydown', function (event) {
//     if (event.key == 'ArrowLeft') {
//         makeSelection("Altered");
//     }
//     else if (event.key == 'ArrowRight') {
//         makeSelection("Original");
//     }
// });

async function makeSelection(userSelection) {
    try {
        const response = await fetch('http://localhost:3000/userInput', {
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
        return response;
    } catch (error) {
        console.error('Error:', error);
        alert("Error sending request: " + error);
    }
    
}

async function getRandomImage() {
    const baseUrl = 'http://localhost:3000/randomImage';
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
