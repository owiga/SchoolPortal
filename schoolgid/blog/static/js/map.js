const map = L.map('map', {
    crs: L.CRS.Simple, // Используем плоскую карту
    minZoom: -2, // Масштаб
});

const bounds = [[0, 0], [1000, 1000]]; // Размер карты в пикселях
const image = L.imageOverlay('../media/ffloor.png', bounds).addTo(map);
map.fitBounds(bounds);

// Добавляем метку кабинета
L.marker([500, 500]).addTo(map).bindPopup("Кабинет 101");
L.marker([700, 600]).addTo(map).bindPopup("Кабинет 102");