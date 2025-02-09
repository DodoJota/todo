document.addEventListener('DOMContentLoaded', function() {
    // Manipula a mudança no checkbox de conclusão
    const todoList = document.getElementById('todo-list');
    todoList.addEventListener('change', function(event) {
        if (event.target.classList.contains('complete-checkbox')) {
            const checkbox = event.target;
            const li = checkbox.closest('li');
            const todoId = li.getAttribute('data-id');
            const completed = checkbox.checked;

            fetch('/complete/' + todoId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ completed: completed })
            })
            .then(response => {
                return response.json().then(data => {
                    if (!response.ok) {
                        // Se a resposta não for ok (status HTTP não está na faixa 200-299)
                        throw { status: response.status, message: data.message, category: data.category || 'error' };
                    }
                    return data;
                });
            })
            .then(data => {
                // Atualiza a interface com base na resposta
                const todoContent = li.querySelector('.todo-content');
                if (completed) {
                    todoContent.classList.add('completed');
                } else {
                    todoContent.classList.remove('completed');
                }
                showFlashMessage(data.message, data.category);
            })
            .catch(error => {
                console.error('Erro:', error);
                showFlashMessage(error.message || 'Erro desconhecido.', error.category || 'error');
                checkbox.checked = !completed; // Reverter o estado do checkbox em caso de erro
            });
        }
    });

    // Manipula o clique no botão de excluir
    todoList.addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-button')) {
            const button = event.target;
            const li = button.closest('li');
            const todoId = li.getAttribute('data-id');

            fetch('/delete/' + todoId, {
                method: 'POST',
            })
            .then(response => {
                return response.json().then(data => {
                    if (!response.ok) {
                        throw { status: response.status, message: data.message, category: data.category || 'error' };
                    }
                    return data;
                });
            })
            .then(data => {
                // Remove a tarefa da interface
                li.remove();
                showFlashMessage(data.message, data.category);
            })
            .catch(error => {
                console.error('Erro:', error);
                showFlashMessage(error.message || 'Erro desconhecido.', error.category || 'error');
            });
        }
    });

    // Função para exibir mensagens flash
    function showFlashMessage(message, category) {
        const existingFlashes = document.querySelector('.flashes');
        const flashMessage = document.createElement('li');
        flashMessage.className = category;
        flashMessage.textContent = message;

        if (existingFlashes) {
            existingFlashes.appendChild(flashMessage);
        } else {
            const flashesList = document.createElement('ul');
            flashesList.className = 'flashes';
            flashesList.appendChild(flashMessage);
            const container = document.querySelector('.container') || document.body;
            container.insertBefore(flashesList, container.firstChild);
        }

        // Remove a mensagem flash após algum tempo
        setTimeout(() => {
            flashMessage.remove();
            const flashes = document.querySelector('.flashes');
            if (flashes && flashes.children.length === 0) {
                flashes.remove();
            }
        }, 3000);
    }
});