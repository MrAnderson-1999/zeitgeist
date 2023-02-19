function generateImage() {
    // send a request to the server to generate an image
    fetch('/generate_image')
        .then(response => response.json())
        .then(data => {
            // update the image on the webpage
            let imageElement = document.createElement('img');
            imageElement.src = data.url;
            imageElement.style.position = 'absolute';
            imageElement.style.left = data.x + 'px';
            imageElement.style.top = data.y + 'px';
            imageElement.style.width = data.width + 'px';
            imageElement.style.height = data.height + 'px';
            document.getElementById('smiley-face').innerHTML = '';
            document.getElementById('smiley-face').appendChild(imageElement);
        });
}

// generate the initial image
generateImage();

// generate a new image every minute
setInterval(generateImage, 60000);

// submit the survey form
document.getElementById('survey-form').addEventListener('submit', (event) => {
    event.preventDefault();

    let formData = new FormData(event.target);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/submit_survey');
    xhr.onload = () => {
        if (xhr.status === 200) {
            alert('Your survey has been submitted successfully!');
        } else {
            alert('There was an error submitting your survey. Please try again later.');
        }
    };
    xhr.send(formData);
});
