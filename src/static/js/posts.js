document.getElementById('createPostForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const communityId = parseInt(this.dataset.communityId); // Получаем community_id из атрибута формы

    // Проверяем, что community_id является корректным числом
    if (isNaN(communityId)) {
        alert('Invalid community ID.');
        return;
    }

    console.log('Content:', formData.get('content'));
    console.log('Community ID:', communityId);

    try {
        const response = await fetch('/api/v1/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: formData.get('content'), // Передаем content
                community_id: communityId, // Передаем community_id
            }),
        });

        if (response.ok) {
            window.location.reload(); // Перезагружаем страницу для отображения нового поста
        } else {
            const errorData = await response.json();
            alert('Failed to create post: ' + (errorData.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while creating the post. Please try again.');
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