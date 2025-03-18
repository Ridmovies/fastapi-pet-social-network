 // Логика для кнопок Edit, Save, Cancel
        document.getElementById('editButton').addEventListener('click', function () {
            // Активируем текстовое поле
            document.getElementById('postContent').disabled = false;
            // Активируем кнопки Save и Cancel
            document.getElementById('saveButton').disabled = false;
            document.getElementById('cancelButton').disabled = false;
            // Деактивируем кнопку Edit
            this.disabled = true;
        });

        document.getElementById('cancelButton').addEventListener('click', function () {
            // Возвращаем текстовое поле в исходное состояние
            document.getElementById('postContent').disabled = true;
            document.getElementById('postContent').value = `{{ post.content }}`;  // Восстанавливаем исходное содержимое
            // Деактивируем кнопки Save и Cancel
            document.getElementById('saveButton').disabled = true;
            document.getElementById('cancelButton').disabled = true;
            // Активируем кнопку Edit
            document.getElementById('editButton').disabled = false;
        });

        document.getElementById('editPostForm').addEventListener('submit', async function (e) {
            e.preventDefault(); // Предотвращаем отправку формы
            const postId = this.querySelector('#editButton').dataset.postId; // Получаем ID поста
            const newContent = document.getElementById('postContent').value;

            try {
                // Отправляем PATCH-запрос на сервер
                const response = await fetch(`/api/v1/post/${postId}`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ content: newContent }),
                });

                if (!response.ok) {
                    throw new Error('Failed to update the post');
                }

                // Уведомляем пользователя об успешном обновлении
                alert('Post updated successfully!');
                // Деактивируем текстовое поле и кнопки
                document.getElementById('postContent').disabled = true;
                document.getElementById('saveButton').disabled = true;
                document.getElementById('cancelButton').disabled = true;
                // Активируем кнопку Edit
                document.getElementById('editButton').disabled = false;
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to update the post. Please try again.');
            }
        });