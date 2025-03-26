// post_create.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createPostForm');

    if (form) {
        form.addEventListener('submit', async function(event) {
            event.preventDefault();

            // Получаем элементы формы
            const submitButton = form.querySelector('button[type="submit"]');
            const contentTextarea = form.querySelector('#content');
            const fileInput = form.querySelector('#image');

            // Валидация контента
            if (!contentTextarea.value.trim()) {
                alert('Please enter post content');
                return;
            }

            // Показываем индикатор загрузки
            submitButton.disabled = true;
            submitButton.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Posting...
            `;

            try {
                // Создаем FormData и добавляем все поля
                const formData = new FormData();
                formData.append('content', contentTextarea.value.trim());
                formData.append('community_id', '1'); // Значение по умолчанию

                // Добавляем файл, если он выбран
                if (fileInput.files[0]) {
                    formData.append('image', fileInput.files[0]);
                }

                // Отправляем запрос
                const response = await fetch('api/v1/post', {
                    method: 'POST',
                    body: formData
                    // Не устанавливаем Content-Type - браузер сделает это автоматически
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Failed to create post');
                }

                // Успешно - перезагружаем страницу
                window.location.reload();

            } catch (error) {
                console.error('Error:', error);
                alert('Error: ' + error.message);
            } finally {
                // Восстанавливаем кнопку
                submitButton.disabled = false;
                submitButton.textContent = 'Submit';
            }
        });
    }

    // Опционально: предпросмотр изображения перед отправкой
    const imagePreview = document.createElement('img');
    imagePreview.style.maxWidth = '100%';
    imagePreview.style.marginTop = '10px';
    imagePreview.style.display = 'none';
    document.querySelector('#image').parentNode.appendChild(imagePreview);

    document.getElementById('image').addEventListener('change', function(e) {
        if (e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = function(event) {
                imagePreview.src = event.target.result;
                imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(e.target.files[0]);
        } else {
            imagePreview.style.display = 'none';
        }
    });
});