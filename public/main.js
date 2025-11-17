let imageFilename = "";

window.onload = function () {
    getRandomImage();
}


document.addEventListener('keydown', function (event) {
    if (event.key == 'ArrowLeft') {
        alert('Left was pressed');
    }
    else if (event.key == 'ArrowRight') {
        alert('Right was pressed');
    }
});

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
    try {
        const response = await fetch('http://localhost:3000/randomImage', {
            method: "GET",
        });
        imageFilename = response.headers.get('X-Image-Filename');
        const baseUrl = response.url;
        const timestamp = new Date().getTime();
        const uniqueUrl = `${baseUrl}?t=${timestamp}`;
        document.getElementById("rand_img").src = uniqueUrl;
        
        return response;
    } catch (error) {
        console.error('Error:', error);
        alert("Error sending request: " + error);
    }
}
