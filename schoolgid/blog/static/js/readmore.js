document.querySelectorAll(".post-read-more-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      let textId = this.dataset.text; // Берем ID текста из data-text
      let textContainer = document.getElementById(textId);

      if (textContainer.classList.toggle("expanded")) {
        this.textContent = "Скрыть";
        this.style.display = 'none';
      } else {
        this.textContent = "Читать дальше";
      }
    });
  });