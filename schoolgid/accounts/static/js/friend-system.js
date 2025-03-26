
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".add-friend-btn").forEach(button => {
        button.addEventListener("click", function() {
            let userId = this.dataset.userId;
            let userUsername = this.dataset.username;
            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
            console.log("Добавляем в друзья:", userUsername, "(ID:", userId, ")", csrfToken);
            
            fetch(`/profile/${userUsername}/send_friend_request/${userId}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({})
            })
            .then(response => {
                console.log(response)
                if (response.ok) {
                    console.log("Успех!")   
                    return response.json();
                }
                throw new Error("Ошибка при отправке запроса");
            })
            .then(data => {
                this.textContent = "Удалить заявку";
                this.classList.add("cancel-friend-btn");
                this.classList.remove("add-friend-btn");
                location.reload();
            })
            .catch(error => console.error(error));
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".cancel-friend-btn").forEach(button => {
        button.addEventListener("click", function() {
            let userId = this.dataset.userId;
            let userUsername = this.dataset.username;
            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
            
            fetch(`/profile/${userUsername}/cancel_friend_request/${userId}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({})
            })
            .then(response => {
                console.log(response)
                if (response.ok) {
                    console.log("Успех!")   
                    return response.json();
                }
                throw new Error("Ошибка при отправке запроса");
            })
            .then(data => {
                this.textContent = "Добавить в друзья";
                this.classList.add("cancel-friend-btn");
                this.classList.remove("add-friend-btn");
                location.reload();
            })
            .catch(error => console.error(error));
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".delete-friend-btn").forEach(button => {
        button.addEventListener("click", function() {
            let userId = this.dataset.userId;
            let userUsername = this.dataset.username;
            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
            
            fetch(`/profile/${userUsername}/delete_friend/${userId}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({})
            })
            .then(response => {
                console.log(response)
                if (response.ok) {
                    console.log("Успех!")   
                    return response.json();
                }
                throw new Error("Ошибка при отправке запроса");
            })
            .then(data => {
                this.textContent = "Добавить в друзья";
                this.classList.add("delete-friend-btn");
                this.classList.remove("add-friend-btn");
                location.reload();
            })
            .catch(error => console.error(error));
        });
    });
});