document.addEventListener("DOMContentLoaded", function () {
    let selectElementGrades = document.getElementById("settings-show-grades-select");
    let selectElementFriends = document.getElementById("settings-show-friends-select");
    const username = document.getElementById("data-user").getAttribute("data-username");

    selectElementGrades.addEventListener("change", function () {
        let selectedValue = this.value;

        fetch(`../../../update_privacy/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()  // Получаем CSRF-токен
            },
            body: JSON.stringify({
                show_grades: selectedValue
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Настройки успешно обновлены!");
            } else {
                console.error("Ошибка:", data.error);
            }
        })
        .catch(error => console.error("Ошибка запроса:", error));
    });

    selectElementFriends.addEventListener("change", function () {
        let selectedValue = this.value;

        fetch(`../../../update_privacy/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()  // Получаем CSRF-токен
            },
            body: JSON.stringify({
                show_friends: selectedValue
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Настройки успешно обновлены!");
            } else {
                console.error("Ошибка:", data.error);
            }
        })
        .catch(error => console.error("Ошибка запроса:", error));
    });

    // Функция для получения CSRF-токена из cookies
    function getCSRFToken() {
        let cookieValue = null;
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                break;
            }
        }
        return cookieValue;
    }
});