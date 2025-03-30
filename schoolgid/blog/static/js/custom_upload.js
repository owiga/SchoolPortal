const realFileBtn = document.getElementById("id_cover");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");
const previewImage = document.getElementById("preview-image");

customBtn.addEventListener("click", function() {
    realFileBtn.click();
});

realFileBtn.addEventListener("change", function() {
    if (realFileBtn.files.length > 0) {
        const file = realFileBtn.files[0];
        customTxt.textContent = "Загружено!";

        // Отображение превью
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewImage.style.display = "block";
        };
        reader.readAsDataURL(file);
    } else {
        customTxt.textContent = "Файл не выбран (Необязательно)";
        previewImage.style.display = "none";
    }
});