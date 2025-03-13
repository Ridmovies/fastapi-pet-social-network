        document.getElementById('loginForm').addEventListener('submit', async function(event) {
            event.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const response = await fetch('/api/v1/users/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
                credentials: 'include'  // Включаем куки в запрос
            });

            if (response.ok) {
                const data = await response.json();
                // Перенаправляем на защищенный эндпоинт
                window.location.href = '/users/me';
            } else {
                const errorData = await response.json();
                document.getElementById('errorMessage').textContent = errorData.detail || 'Login failed';
            }
        });