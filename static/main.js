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
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Atualiza a interface
                    const todoContent = li.querySelector('.todo-content');
                    if (completed) {
                        todoContent.classList.add('completed');
                    } else {
                        todoContent.classList.remove('completed');
                    }
                    showFlashMessage(data.message, data.category);
                } else {
                    // Lida com o erro
                    showFlashMessage(data.message, data.category || 'error');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
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
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Remove a tarefa da interface
                    li.remove();
                    showFlashMessage(data.message, data.category);
                } else {
                    // Lida com o erro
                    showFlashMessage(data.message, data.category || 'error');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
            });
        }
    });

    // Função para exibir mensagens flash
    function showFlashMessage(message, category) {
        const flashes = document.querySelector('.flashes');
        const flashMessage = document.createElement('li');
        flashMessage.className = category;
        flashMessage.textContent = message;
        if (flashes) {
            flashes.appendChild(flashMessage);
        } else {
            const flashesList = document.createElement('ul');
            flashesList.className = 'flashes';
            flashesList.appendChild(flashMessage);
            document.body.insertBefore(flashesList, document.body.firstChild);
        }
        // Remove a mensagem flash após algum tempo
        setTimeout(() => {
            flashMessage.remove();
        }, 3000);
    }
});