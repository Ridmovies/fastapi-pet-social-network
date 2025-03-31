document.getElementById('addCommentForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const eventId = this.dataset.eventId;
    const commentText = document.getElementById('newComment').value.trim();

    if (!commentText) {
        alert('Пожалуйста, введите текст комментария.');
        return;
    }

    try {
        // Отправляем POST-запрос на сервер
        const response = await fetch('/api/v1/comments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: commentText,
                event_id: eventId
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Не удалось отправить комментарий.');
        }

        const newComment = await response.json();

        // Очищаем поле ввода комментария
        document.getElementById('newComment').value = '';

        // Обновляем список комментариев на странице
        const newCommentItem = `
            <li class="list-group-item">
                <strong>{{ user.username }}:</strong> ${commentText}
                <a href="#" class="comment-delete" data-comment-id="${newComment.id}"
                   data-event-id="${eventId}">Удалить</a>
            </li>
        `;

        const commentsList = document.getElementById('commentsList');
        commentsList.insertAdjacentHTML('afterbegin', newCommentItem);

    } catch (error) {
        console.error('Ошибка:', error);
        alert(error.message || 'Произошла ошибка при отправке комментария. Попробуйте еще раз.');
    }
});