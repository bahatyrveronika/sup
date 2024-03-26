document.addEventListener('DOMContentLoaded', function() {
    const starRating = document.querySelector('.star-rating');
    const ratingInputs = starRating.querySelectorAll('input[type="radio"]');
    const feedbackTextarea = document.querySelector('.feedback');
    const submitButton = document.querySelector('.submit-rating');

    let selectedRating = 0;

    // Обробка кліків по зіркам
    starRating.addEventListener('click', function(event) {
        if (event.target.tagName === 'LABEL') {
            selectedRating = parseInt(event.target.getAttribute('for').replace('star', ''));
            updateStars(selectedRating);
        }
    });

    // Оновлення вигляду зірок
    function updateStars(rating) {
        ratingInputs.forEach(input => {
            const starNumber = parseInt(input.getAttribute('id').replace('star', ''));
            if (starNumber <= rating) {
                input.checked = true;
            } else {
                input.checked = false;
            }
        });
    }

    // Обробка відправлення форми
    submitButton.addEventListener('click', function(event) {
        event.preventDefault();
        const feedback = feedbackTextarea.value;

        // Отримання обраного рейтингу і відправка даних
        if (selectedRating > 0) {
            sendRating(selectedRating, feedback);
        } else {
            alert('Please select a rating before submitting.');
        }
    });

    // Функція для відправлення рейтингу на сервер
    function sendRating(rating, feedback) {
        const formData = new FormData();
        formData.append('rating', rating);
        formData.append('feedback', feedback);

        fetch('/submit_review', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            // Додайте код для обробки успішної відправки
            console.log('Rating submitted successfully');
        })
        .catch(error => {
            // Додайте код для обробки помилки
            console.error('There was a problem submitting the rating:', error);
        });
    }
});
