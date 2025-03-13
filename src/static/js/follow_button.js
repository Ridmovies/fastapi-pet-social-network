document.getElementById("follow-button").addEventListener("click", async function () {
    const userId = this.getAttribute("data-user-id");
    const button = this;

    try {
        // Определяем, подписан ли пользователь
        const isFollowing = button.textContent.trim() === "Отписаться";

        // Отправляем запрос на сервер
        const response = await fetch(`/api/v1/users/${userId}/${isFollowing ? "unfollow" : "follow"}`, {
            method: isFollowing ? "DELETE" : "POST",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            // Обновляем текст кнопки
            button.textContent = isFollowing ? "Подписаться" : "Отписаться";

            // Меняем стиль кнопки
            if (isFollowing) {
                button.classList.remove("btn-danger");
                button.classList.add("btn-primary");
            } else {
                button.classList.remove("btn-primary");
                button.classList.add("btn-danger");
            }
        } else {
            alert("Ошибка при выполнении действия");
        }
    } catch (error) {
        console.error("Ошибка:", error);
    }
});