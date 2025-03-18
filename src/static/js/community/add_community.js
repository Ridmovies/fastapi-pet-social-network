    document.getElementById('addCommunityForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Предотвращаем стандартное поведение формы

        const formData = {
            name: document.getElementById('communityName').value.trim(),
            description: document.getElementById('communityDescription').value.trim()
        };

        // Проверка на пустые поля
        if (!formData.name || !formData.description) {
            alert('Please fill in all fields.');
            return;
        }

        try {
            // Отправляем POST-запрос на сервер
            const response = await fetch('/api/v1/community', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            // Проверяем статус ответа
            if (!response.ok) {
                throw new Error('Failed to create community.');
            }

            const newCommunity = await response.json(); // Парсим ответ сервера

            // Очищаем форму
            document.getElementById('addCommunityForm').reset();

            // Добавляем новое сообщество в список
            const communityList = document.getElementById('communityList');
            const newCommunityCard = `
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title">${newCommunity.name}</h5>
                        <p class="card-text">${newCommunity.description}</p>
                    </div>
                </div>
            `;
            communityList.insertAdjacentHTML('afterbegin', newCommunityCard); // Добавляем в начало списка

            alert('Community created successfully!');
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while creating the community. Please try again.');
        }
    });