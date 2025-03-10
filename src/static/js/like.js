// Обработчик для кнопок лайка
document.querySelectorAll('.like-post').forEach(button => {
    button.addEventListener('click', async function () {
        const postId = this.getAttribute('data-post-id');
        const likeIcon = this.querySelector('.like-icon');

        try {
            // Отправка запроса на лайк
            const response = await fetch(`/api/v1/post/${postId}/like`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', // Для отправки куки (если используется аутентификация)
            });

            if (response.ok) {
                const data = await response.json(); // Предположим, что сервер возвращает { isLiked: boolean }

                // Обновляем иконку
                likeIcon.textContent = data.isLiked ? '❤️' : '🤍';
            } else {
                console.error('Ошибка при отправке лайка:', await response.text());
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    });
});