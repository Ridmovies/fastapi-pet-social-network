    document.getElementById('logout-link').addEventListener('click', async function(event) {
        event.preventDefault(); // Отменяем стандартное поведение ссылки

        const response = await fetch('/api/v1/users/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Включаем куки в запрос
        });

        if (response.ok) {
            alert('Logged out successfully!');
            window.location.href = '/'; // Перенаправляем на главную страницу
        } else {
            const errorData = await response.json();
            alert('Failed to logout: ' + (errorData.detail || 'Unknown error'));
        }
    });