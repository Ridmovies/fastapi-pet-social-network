document.getElementById('createPostForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    try {
        const response = await fetch('/api/v1/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: formData.get('content'), // Передаем content
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
