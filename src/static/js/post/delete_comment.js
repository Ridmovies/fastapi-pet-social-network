document.addEventListener("DOMContentLoaded", function () {
    // Находим все элементы с классом "comment-delete"
    const deleteButtons = document.querySelectorAll(".comment-delete");

    // Добавляем обработчик события для каждой кнопки удаления
    deleteButtons.forEach((button) => {
        button.addEventListener("click", async function (event) {
            event.preventDefault(); // Предотвращаем переход по ссылке

            // Получаем ID комментария из атрибута data-comment-id
            const commentId = button.getAttribute("data-comment-id");
            const postId = button.getAttribute("data-post-id");


            // Подтверждение удаления
            const confirmDelete = confirm("Вы уверены, что хотите удалить этот комментарий?");
            if (!confirmDelete) {
                return;
            }

            try {
                // Отправляем DELETE-запрос на сервер
                const response = await fetch(`/api/v1/post/${postId}/comment/${commentId}`, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    // Если удаление успешно, перезагружаем страницу
                    window.location.reload();
                } else {
                    // Если произошла ошибка, выводим сообщение
                    alert("Не удалось удалить комментарий");
                }
            } catch (error) {
                console.error("Ошибка при удалении комментария:", error);
                alert("Произошла ошибка при удалении комментария");
            }
        });
    });
});
