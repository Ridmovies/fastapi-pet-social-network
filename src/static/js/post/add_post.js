    document.getElementById('createPostForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(this);
        const communityId = parseInt(this.dataset.communityId); // Получаем community_id из атрибута формы

        // Проверяем, что community_id является корректным числом
        if (isNaN(communityId)) {
            alert('Invalid community ID.');
            return;
        }

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