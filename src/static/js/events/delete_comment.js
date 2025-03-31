document.addEventListener("DOMContentLoaded", function () {
    // Находим все элементы с классом "comment-delete"
    const deleteButtons = document.querySelectorAll(".comment-delete");

    // Добавляем обработчик события для каждой кнопки удаления
    deleteButtons.forEach((button) => {
        button.addEventListener("click", async function (event) {
            event.preventDefault(); // Предотвращаем переход по ссылке

            // Получаем ID комментария и ID поста/события
            const commentId = button.getAttribute("data-comment-id");
            const postId = button.getAttribute("data-post-id");
            const eventId = button.getAttribute("data-event-id");

            // Подтверждение удаления
            const confirmDelete = confirm("Вы уверены, что хотите удалить этот комментарий?");
            if (!confirmDelete) {
                return;
            }

            try {
                // Определяем endpoint в зависимости от того, к чему привязан комментарий
                let endpoint;
                if (postId) {
                    endpoint = `/api/v1/comments/${commentId}?post_id=${postId}`;
                } else if (eventId) {
                    endpoint = `/api/v1/comments/${commentId}?event_id=${eventId}`;
                } else {
                    throw new Error("Не указан post_id или event_id");
                }

                // Отправляем DELETE-запрос на сервер
                const response = await fetch(endpoint, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    // Если удаление успешно, удаляем элемент из DOM
                    button.closest('li').remove();
                } else {
                    // Если произошла ошибка, выводим сообщение
                    const errorData = await response.json();
                    throw new Error(errorData.detail || "Не удалось удалить комментарий");
                }
            } catch (error) {
                console.error("Ошибка при удалении комментария:", error);
                alert(error.message || "Произошла ошибка при удалении комментария");
            }
        });
    });
});