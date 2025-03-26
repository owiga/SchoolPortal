const dropdownHeader = document.querySelector('.header__profile');
const dropdownContent = document.querySelector('.dropdown-content');
const arrow = document.querySelector('.header__arrow');

console.log('dropdownHeader:', dropdownHeader);
console.log('dropdownContent:', dropdownContent);
console.log('arrow:', arrow);

// Добавляем обработчик события "click" на заголовок
dropdownHeader.addEventListener('click', function () {
    event.stopPropagation();
    dropdownContent.classList.toggle('open'); // Добавляем/удаляем класс
    arrow.classList.toggle('open');
    console.log("all good")
});
        
// Закрываем выпадающий список при клике вне его области
document.addEventListener('click', function (event) {
if (!event.target.closest('.header__block_profile')) {
    dropdownContent.classList.remove('open');
    arrow.classList.remove('open');
}
});
        
if (!dropdownHeader || !dropdownContent) {
console.error('Элементы не найдены!');
}