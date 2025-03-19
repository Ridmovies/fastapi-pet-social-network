        document.getElementById('registerForm').addEventListener('submit', async function(event) {
            event.preventDefault();

            const username = document.getElementById('username').value; // Изменено на email
            const password = document.getElementById('password').value;

            const response = await fetch('/api/v1/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username, // Изменено на email
                    password: password,
                    is_active: true,      // Добавлено
                }),
            });

            if (response.ok) {
                const data = await response.json();
                alert('Registration successful!');
                window.location.href = '/users/login';  // Перенаправление на страницу входа
            } else {
                const errorData = await response.json();
                document.getElementById('errorMessage').textContent = errorData.detail || 'Registration failed';
            }
        });