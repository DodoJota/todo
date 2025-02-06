document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const todoId = checkbox.getAttribute('data-id');
            const completed = checkbox.checked;

            fetch(`/complete/${todoId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ completed: completed }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const span = checkbox.parentElement.querySelector('span');
                    if (completed) {
                        span.style.textDecoration = 'line-through';
                    } else {
                        span.style.textDecoration = 'none';
                    }
                    // Adiciona a mensagem flash sem precisar recarregar
                    const flashMessage = document.createElement('li');
                    flashMessage.className = `flash-message ${data.category}`;
                    flashMessage.textContent = data.message;
                    document.querySelector('.flashes').appendChild(flashMessage);
                    
                    // Remove a mensagem flash após 3 segundos
                    setTimeout(() => {
                        flashMessage.style.transition = 'opacity 0.5s ease-out';
                        flashMessage.style.opacity = '0';
                        setTimeout(() => {
                            flashMessage.remove();
                        }, 500);
                    }, 3000);
                }
            })
            .catch(error => console.error('Erro:', error));
        });
    });
});