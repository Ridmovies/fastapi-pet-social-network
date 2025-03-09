        document.getElementById('createPostForm').addEventListener('submit', async function(event) {
            event.preventDefault();

            const formData = new FormData(this);
            const response = await fetch('/api/v1/post', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: formData.get('content'),
                }),
            });

            if (response.ok) {
<!--                alert('Post created successfully!');-->
                window.location.reload(); // Перезагружаем страницу для отображения нового поста
            } else {
                const errorData = await response.json();
                alert('Failed to create post: ' + (errorData.detail || 'Unknown error'));
            }
        });

      // Скрипт для удаления поста через Fetch API

    // Обработчик для кнопок удаления
document.querySelectorAll('.delete-post').forEach(button => {
    button.addEventListener('click', async function() {
        const postId = this.getAttribute('data-post-id');

        // Подтверждение удаления
        const isConfirmed = confirm('Are you sure you want to delete this post?');
        if (!isConfirmed) {
            return; // Если пользователь отменил, ничего не делаем
        }

        // Отправка запроса на удаление
        const response = await fetch(`/api/v1/post/${postId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            window.location.reload(); // Перезагружаем страницу для обновления списка постов
        } else {
            const errorData = await response.json();
            alert('Failed to delete post: ' + (errorData.detail || 'Unknown error'));
        }
    });
});