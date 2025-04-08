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