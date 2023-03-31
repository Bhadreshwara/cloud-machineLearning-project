const form = document.querySelector('form');
const imageInput = document.querySelector('#image');
const nameDiv = document.querySelector('#name');
const emailDiv = document.querySelector('#email');
const resultsDiv = document.querySelector('#results');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const file = imageInput.files[0];
    const formData = new FormData();
    formData.append('image', file);

    const response = await fetch('/business-cards', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    // Update the results div with the extracted data
    nameDiv.innerText = `Name: ${data.name}`;
    emailDiv.innerText = `Email: ${data.email}`;
    resultsDiv.classList.add('show');
});
