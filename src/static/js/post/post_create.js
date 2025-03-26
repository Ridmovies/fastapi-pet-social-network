// post_create.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createPostForm');

    if (!form) return;

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        // Получаем элементы формы
        const submitButton = form.querySelector('button[type="submit"]');
        const content = form.querySelector('#content').value.trim();

        // Валидация контента
        if (!content) {
            alert('Please enter post content');
            return;
        }

        // Показываем индикатор загрузки
        submitButton.disabled = true;
        submitButton.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status"></span>
            Posting...
        `;

        try {
            // Собираем данные формы
            const formData = new FormData(form);

            // Отправляем запрос
            const response = await fetch('/api/v1/post', {
                method: 'POST',
                body: formData
            });

            // Обрабатываем ответ
            if (response.ok) {
                // Успешный ответ - редирект
                window.location.href = '/posts';
            } else {
                // Ошибка сервера
                const error = await response.json();
                throw new Error(error.detail || 'Failed to create post');
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Error: ' + error.message);
        } finally {
            // Восстанавливаем кнопку
            submitButton.disabled = false;
            submitButton.textContent = 'Submit';
        }
    });
});