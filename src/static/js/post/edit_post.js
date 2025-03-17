document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM загружен'); // Проверка загрузки DOM

    const editButton = document.querySelector('.edit-post');
    if (editButton) {
        console.log('Кнопка "Редактировать" найдена'); // Проверка, что кнопка существует
        editButton.addEventListener('click', function () {
            console.log('Кнопка "Редактировать" нажата'); // Проверка, что событие срабатывает

            // Получаем элементы
            const postContent = document.getElementById('post-content');
            const editContent = document.getElementById('edit-content');
            const editForm = document.getElementById('edit-form');

            // Проверяем, что элементы существуют
            if (postContent && editContent && editForm) {
                editContent.value = postContent.innerText; // Копируем текст поста в текстовое поле
                editForm.style.display = 'block'; // Показываем форму редактирования
            } else {
                console.error('Один из элементов не найден'); // Ошибка, если элемент не найден
            }
        });
    } else {
        console.error('Кнопка "Редактировать" не найдена'); // Ошибка, если кнопка не найдена
    }
});