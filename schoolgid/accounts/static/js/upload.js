function updateFileName() {
    let fileInput = document.getElementById("reg-cover");
    let fileText = document.getElementById("fileText");
    let BtnBackground = document.getElementById("reg-l-cover"); 
    let fileUploadedText = document.getElementById("fileTextBefore");

    if (fileInput.files.length > 0) {
      let file = fileInput.files[0];
  
      // Проверяем, что файл является изображением
      if (file.type.startsWith('image/')) {
        let reader = new FileReader();
  
        reader.onload = function(event) {
          // Обновляем фон
          BtnBackground.style.backgroundImage = `url(${event.target.result})`;
          BtnBackground.style.backgroundSize = 'cover';
          BtnBackground.style.backgroundPosition = 'center'; // Центрируем изображение
          BtnBackground.style.backgroundRepeat = 'no-repeat'; // Убираем повторение
        };
  
        reader.readAsDataURL(file);
        fileText.textContent = "";
        fileUploadedText.textContent = "Изображение загружено!"; // Очищаем текст
      } else {
        fileText.textContent = "Выберите изображение"; // Если файл не изображение
      }
    } else {
      fileText.textContent = "+"; // Если файл не выбран
      BtnBackground.style.backgroundImage = ""; // Убираем фоновое изображение
      fileUploadedText.textContent = "Загрузить аватар"
    }
  }