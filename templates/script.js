const playerNames = JSON.parse('{{ player_names|default("[]")|tojson|safe }}');
            const inputElement = document.querySelector('input[name="guess"]');
            const datalistElement = document.createElement('datalist');
            datalistElement.id = 'playerNames';
            inputElement.setAttribute('list', 'playerNames');
            document.body.appendChild(datalistElement);
          
            function updateAutocomplete() {
              const inputValue = inputElement.value.toLowerCase();
              const suggestions = playerNames.filter((name) =>
                name.toLowerCase().startsWith(inputValue)
              );
              datalistElement.innerHTML = suggestions
                .map((name) => `<option value="${name}"></option>`)
                .join('');
            }
          
            // inputElement.addEventListener('input', updateAutocomplete);
            inputElement.addEventListener('input', function () {
                updateAutocomplete();
                inputElement.classList.toggle('filled', inputElement.value.trim() !== '');
            });