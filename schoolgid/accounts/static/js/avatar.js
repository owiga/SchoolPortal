document.getElementById('avatar-upload').addEventListener('change', function(event) {
    let file = event.target.files[0];
    if (file) {
        let preview = document.getElementById('avatar-preview');
        preview.src = URL.createObjectURL(file); // Создаем временную ссылку на файл
        document.getElementById('submit-button').style.display = 'flex';
    }
});

document.getElementById('change-avatar').addEventListener('click', function() {
    document.getElementById('avatar-upload').click(); // Открываем диалог выбора файла
});