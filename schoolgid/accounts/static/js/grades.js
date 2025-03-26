let username = document.getElementById("user-info").dataset.username;
let teacher_lesson = document.getElementById("user-info2").dataset.username;
let teacher_id = document.getElementById("user-info3").dataset.username;
let today = new Date();
let month = today.getMonth() + 1;

function fetchUsers(classroom = null) {
    let url = `../../../profile/${username}/filter_users/`;
    if (classroom) {
        url += `?classroom=${classroom}`;
    }

    fetch(url)
    .then(response => response.json())
    .then(data => {
        let userList = document.getElementById('user-list');
        userList.innerHTML = ""; // Очищаем список

        if (data.users.length === 0) { 
            // Если пользователей нет, выводим сообщение
            let tr = document.createElement('tr');
            let td = document.createElement('td');
            td.setAttribute('colspan', '1'); // Охватываем все столбцы
            td.textContent = "Нет учеников";
            td.style.textAlign = "center";
            td.style.color = '#ff9e9e';
            tr.appendChild(td);
            userList.appendChild(tr);
        } else {
            // Если есть ученики, отображаем их
            data.users.forEach(user => {
                let tr = document.createElement('tr');
                tr.id = 'user-item';
                let td = document.createElement('td');
                td.textContent = `${user.first_name} ${user.last_name}`;
                tr.appendChild(td);

                for (let i = 0; i < 31; i++) { 
                    let tdSpace = document.createElement('td');
                    tdSpace.id = 'user-item-inp';

                    let form = document.createElement('form');
                    form.method = "GET";

                    let inp = document.createElement('input');
                    inp.type = 'number';
                    inp.name = `${user.id}.${i + 1}.${month}`;
                    inp.min = 2;
                    inp.max = 5;
                    inp.step = 1;
                    inp.required = true;

                    // Подставляем оценку из БД (если есть)
                    let key = `${user.id}.${i + 1}`;
                    if (data.grades[key]) {
                        inp.value = data.grades[key];
                    }

                    form.id = 'grades-user-set';
                    form.appendChild(inp);
                    tdSpace.appendChild(form);
                    tr.appendChild(tdSpace);
                }

                userList.appendChild(tr);
            });
        }
    })
}


document.getElementById('grades-class-select').addEventListener('change', function() {
    let classroom = this.value;
    fetchUsers(classroom);
});


document.addEventListener("DOMContentLoaded", function () {
    fetchUsers('10Т');
});

    document.addEventListener('input', function(event) {
        if (event.target.tagName === 'INPUT') { 
            let form = event.target.closest('form'); // Получаем родительскую форму
            
            if (form) {
                console.log(`Форма ID: ${form.id}, Изменённый инпут: ${event.target.name}, Значение: ${event.target.value}`);
            }
        }
    });
    
    // Отключаем перезагрузку страницы при нажатии Enter
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && event.target.tagName === 'INPUT') {
            event.preventDefault(); // ❗ Предотвращаем стандартную отправку формы
            
            let form = event.target.closest('form'); 
            if (form) {
                let info = event.target.name.split('.')
                let userId = info[0]; // Предполагаем, что ID пользователя передан в data-user-id
                let lessonName = teacher_lesson; // ID предмета (если нужно)
                let date = `${info[1]}.${info[2]}`; // Дата оценки
                let grade = event.target.value; // Значение оценки
                fetch('/grades/save_grade/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken() // Получаем CSRF-токен
                    },
                    body: JSON.stringify({
                        user_id: userId,
                        lesson_id: lessonName,
                        date: date,
                        grade: grade,
                        teacher_id: teacher_id
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('Оценка сохранена:', data);
                    } else {
                        console.error('Ошибка при сохранении:', data.error);
                    }
                })
                .catch(error => console.error('Ошибка запроса:', error));
            }
        }
    });



    function getCSRFToken() {
        let cookieValue = null;
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                cookieValue = cookie.substring('csrftoken='.length, cookie.length);
                break;
            }
        }
        return cookieValue;
    }

    