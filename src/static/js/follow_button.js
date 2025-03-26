// follow_button.js
document.addEventListener('DOMContentLoaded', function() {
    const followButton = document.getElementById('follow-button');

    if (followButton) {
        followButton.addEventListener('click', async function() {
            const followUserId = this.dataset.userId || '{{ follow_user.id }}';
            const isFollowing = this.textContent.trim() === 'Отписаться';
            const apiUrl = isFollowing
                ? `/api/v1/users/${followUserId}/unfollow`
                : `/api/v1/users/${followUserId}/follow`;

            try {
                const response = await fetch(apiUrl, {
                    method: isFollowing ? 'DELETE' : 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}'  // Если используете CSRF защиту
                    },
                    credentials: 'include'  // Для передачи куков, если нужна авторизация
                });

                if (response.ok) {
                    // Обновляем текст и стиль кнопки
                    this.textContent = isFollowing ? 'Подписаться' : 'Отписаться';
                    this.classList.toggle('btn-danger');
                    this.classList.toggle('btn-primary');

                    // Можно добавить уведомление об успехе
                    console.log(isFollowing ? 'Unfollowed successfully' : 'Followed successfully');
                } else {
                    const errorData = await response.json();
                    console.error('Error:', errorData.detail || 'Unknown error');
                    // Можно показать alert или toast-уведомление
                }
            } catch (error) {
                console.error('Network error:', error);
                alert('Network error, please try again');
            }
        });
    }
});