document.getElementById('addCommentForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const postId = this.dataset.postId; // Получаем ID поста из атрибута data-post-id формы
    const commentText = document.getElementById('newComment').value.trim();

    if (!commentText) {
        alert('Пожалуйста, введите текст комментария.');
        return;
    }

    try {
        // Отправляем POST-запрос на сервер
        const response = await fetch(`/api/v1/post/${postId}/comment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: commentText
            })
        });


        if (!response.ok) {
            throw new Error('Не удалось отправить комментарий.');
        }

        // Очищаем поле ввода комментария
        document.getElementById('newComment').value = '';

        // Обновляем список комментариев на странице
        const currentUserEmail = '{{ current_user.email }}'; // Предполагается, что переменная current_user доступна в шаблоне
        const newCommentItem = `
            <li class="list-group-item">
                <strong>${currentUserEmail}:</strong> ${commentText}
            </li>
        `;

        const commentsList = document.getElementById('commentsList');
        commentsList.insertAdjacentHTML('beforeend', newCommentItem);

        alert('Комментарий отправлен успешно!');
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке комментария. Попробуйте еще раз.');
    }
});