document.addEventListener('DOMContentLoaded', function() {
    // Инициализация datetime picker
    flatpickr(".datetimepicker", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true,
        locale: "ru",
        minDate: "today"
    });

    // Обработка формы
    const eventForm = document.getElementById('eventForm');
    const successAlert = document.getElementById('successAlert');

    eventForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Сброс ошибок
        document.querySelectorAll('.error-message').forEach(el => el.textContent = '');

        // Сбор данных формы
        const formData = {
            title: document.getElementById('title').value,
            description: document.getElementById('description').value || null, // Пустое значение → null
            start_datetime: document.getElementById('start_datetime').value,
            end_datetime: document.getElementById('end_datetime').value || null, // Пустое значение → null
            location: document.getElementById('location').value || null, // Пустое значение → null
            is_private: document.getElementById('is_private').checked,
            status: "planned"
        };

        // Валидация (только обязательные поля)
        let isValid = true;
        if (!formData.title) {
            document.getElementById('titleError').textContent = 'Название обязательно';
            isValid = false;
        }
        if (!formData.start_datetime) {
            document.getElementById('startError').textContent = 'Дата начала обязательна';
            isValid = false;
        }

        // Поля end_datetime и location теперь не требуют валидации, так как они optional

        if (!isValid) return;

        try {
            // Отправка на сервер
            const response = await fetch('/api/v1/events', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Ошибка при создании мероприятия');
            }

            const result = await response.json();

            // Показываем сообщение об успехе
            successAlert.classList.remove('d-none');
            eventForm.reset();

            // Через 3 секунды скрываем сообщение
            setTimeout(() => {
                successAlert.classList.add('d-none');
            }, 3000);

            // Можно перенаправить на страницу события
            // window.location.href = `/events/${result.id}`;

        } catch (error) {
            alert(`Ошибка: ${error.message}`);
            console.error('Error:', error);
        }
    });
});