document.addEventListener('DOMContentLoaded', function () {
    // Получаем текущий хеш URL
    let currentTab = window.location.hash ? window.location.hash.substring(1) : 'tab1';

    // Устанавливаем начальное состояние вкладки
    showTab(currentTab);

    // Добавляем обработчик кликов на все ссылки с классом 'tab-link'
    document.body.addEventListener('click', function (event) {
        if (event.target.classList.contains('tab-link')) {
            event.preventDefault();
            let tabId = event.target.getAttribute('data-tab');

            // Обновляем URL без перезагрузки страницы
            window.history.pushState({ tab: tabId }, '', '#' + tabId);

            // Отображаем нужную вкладку
            showTab(tabId);
        }
    });

    // Обработчик для возврата назад в истории
    window.addEventListener('popstate', function (event) {
        if (event.state && event.state.tab) {
            showTab(event.state.tab);
        }
    });

    function showTab(tabId) {
        // Скрываем все вкладки
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });

        // Показываем нужную вкладку
        let activeTab = document.getElementById(tabId);
        if (activeTab) {
            activeTab.classList.add('active');
        }
    }
});
