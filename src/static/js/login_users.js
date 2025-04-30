document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const loginData = {
        grant_type: "password",
        username: email,
        password: password,
        scope: "",
        client_id: "",
        client_secret: ""
    };

    // Преобразуем объект в URL-encoded строку
    const formBody = Object.keys(loginData).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(loginData[key])).join('&');

    const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formBody,
        credentials: 'include'  // Включаем куки в запрос
    });

    if (response.status === 204) {
        // Перенаправляем на защищенный эндпоинт
        window.location.href = '/';
    } else {
        const errorData = await response.json();
        document.getElementById('errorMessage').textContent = errorData.detail || 'Login failed';
    }
});

// Add Google login functionality
document.getElementById('googleLogin').addEventListener('click', async function() {
    console.log("Google login button clicked"); // Проверка, что событие срабатывает
    try {
        const response = await fetch('/api/v1/auth/google/authorize', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
            credentials: 'include'
        });

        if (response.ok) {
            const data = await response.json();
            // Redirect to Google's authorization URL
            window.location.href = data.authorization_url;
        } else {
            const errorData = await response.json();
            document.getElementById('errorMessage').textContent = errorData.detail || 'Failed to initiate Google login';
        }
    } catch (error) {
        document.getElementById('errorMessage').textContent = 'An error occurred during Google login';
        console.error('Google login error:', error);
    }
});