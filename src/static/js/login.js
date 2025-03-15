document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const loginData = {
        grant_type: "password",
        username: username,
        password: password,
        scope: "",
        client_id: "",
        client_secret: ""
    };

    // Преобразуем объект в URL-encoded строку
    const formBody = Object.keys(loginData).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(loginData[key])).join('&');

    const response = await fetch('/api/v1/auth/jwt/login', {
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