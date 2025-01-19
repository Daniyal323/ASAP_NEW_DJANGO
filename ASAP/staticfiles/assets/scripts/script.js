document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Example of basic validation
    if (username === '' || email === '' || password === '') {
        alert('Please fill in all fields.');
        return;
    }

    // Implement signup logic here (e.g., send data to a server)
    alert('Signup successful!');
    
    // Optionally, redirect to a different page after signup
    // window.location.href = 'welcome.html';
});
