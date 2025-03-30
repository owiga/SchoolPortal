document.getElementById("id_title").addEventListener("input", function() {
    document.getElementById("preview-title").textContent = this.value || "Заголовок";
});

document.getElementById("id_content").addEventListener("input", function() {
    document.getElementById("preview-content").textContent = this.value || "Текст новости...";
});

document.getElementById("id_cover").addEventListener("change", function(event) {
    const file = event.target.files[0];
    const previewImage = document.getElementById("preview-cover");

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewImage.style.display = "block";
        };
        reader.readAsDataURL(file);
        const empty = document.getElementById("preview-cover-empty").style.display = 'none';
    } else {
        previewImage.style.display = "none";
    }
});

document.getElementById("news-add-author").addEventListener("change", function() {
    let selectedValue = this.value;
    let cover = document.getElementById("preview-cover-image"); 
    let name = document.getElementById("preview-names");
    if (selectedValue === "anonymous") {
        cover.src = document.getElementById('anonymous-src').getAttribute('data-src');
        name.innerText = "Школа №35";
    }
    else {
        cover.src = document.getElementById('user-cover-1').getAttribute('data-cover');
        name.innerText = document.getElementById('user-name-1').getAttribute('data-names');
    }
})

function getCurrentDateTime() {
    let now = new Date();
    
    let options = { 
        day: '2-digit', 
        month: 'long', 
        year: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    };
    
    let formattedDate = now.toLocaleString('ru-RU', options);
    const timestamp = document.getElementById('time');
    timestamp.innerText = formattedDate;
}
getCurrentDateTime();