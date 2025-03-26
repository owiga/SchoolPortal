const CLASS_MAP = {
    'А': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    'Б': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    'В': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    'Г': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
    'Д': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    'К': ['5', '6', '7', '8', '9'],
    'Т': ['7', '8', '9', '10', '11']
};

// Правильно находим select-элементы
const letterSelect = document.querySelector('#letter-select'); 
const numberSelect = document.querySelector('#number-select');

if (!letterSelect || !numberSelect) {
    console.error('Элементы не найдены! Проверьте ID полей.');
}

function updateNumberOptions(letter) {
    numberSelect.innerHTML = ''; // Очищаем список

    if (CLASS_MAP[letter]) {
        CLASS_MAP[letter].forEach((num, index) => {
            const option = document.createElement('option');
            option.value = num;
            option.textContent = num;
            if (index === 0) option.selected = true; // Делаем первую цифру выбранной
            numberSelect.appendChild(option);
        });

        numberSelect.disabled = false; // Разблокируем поле
    } else {
        numberSelect.disabled = true; // Блокируем, если нет значений
    }
}

// Навешиваем обработчик на изменение буквы
letterSelect.addEventListener('change', function () {
    updateNumberOptions(this.value);
});