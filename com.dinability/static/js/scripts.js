// cannot run JSON in vs code preview
// form-data api
/*function handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.target);
    const value = Object.fromEntries(data.entries());
    // this passes into json????
    console.log({ value });
    // pass json thru python
    // get json back from python
    // return if able to enter
}

*/

function login() {
    // Get the user's email, username, and password from the form
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("psw").value;

    // Create a JSON object with the user's email, username, and password
    var data = { "username": name, "email": email, "password": password };

    // Send a POST request to the API endpoint with the JSON data
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            // Redirect the user to their profile page
            window.location.href = '/profile';
        } else {
            // Display an error message to the user
            alert('Invalid credentials. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function register() {
    // Get the user's email, username, and password from the form
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("psw").value;

    // Create a JSON object with the user's email, username, and password
    var data = { "username": name, "email": email, "password": password };

    // Send a POST request to the API endpoint with the JSON data
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            // Redirect the user to their profile page
            window.location.href = '/login';
        } else {
            // Display an error message to the user
            alert('Invalid credentials. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

const form = document.querySelector('form');
// form.addEventListener('Login', login());
form.addEventListener('Register', register());