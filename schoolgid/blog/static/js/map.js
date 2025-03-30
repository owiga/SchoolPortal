let first_floor = document.getElementById("first-floor").getAttribute("data-map");
let second_floor = document.getElementById("second-floor").getAttribute("data-map");
let third_floor = document.getElementById("third-floor").getAttribute("data-map");

const roomsInfo = {
    "Кабинет 113": "Кабинет биологии/химии.<br> Здесь изучают ботанику и химические реакции.",
    "Кабинет 212": "Кабинет ОБЗР.<br> Здесь рассказывают о ЧС, правилах при опасности и пр.",
    "Кабинет 211": "Кабинет начальных классов.",
    "Кабинет 128": "Кабинет географии.<br> Здесь изучают карты и климат.",
    "Кабинет 127": "Кабинет биологии.<br> Здесь изучают анатомию и ботанику.",
    "Кабинет 126": "Кабинет математики.<br> Здесь изучают   алгебру, геометрию и вероятности.",
    "Кабинет 125": "Кабинет русского языка и литературы.<br> Здесь изучают грамматику и пунктуацию.",
    "Кабинет 124": "Кабинет английского.<br> Здесь изучают английский язык.",
    "Кабинет 123": "Кабинет математики.<br> Здесь изучают алгебру, геометрию и вероятности.",
    "Кабинет 122": "Кабинет математики.<br> Здесь изучают алгебру, геометрию и вероятности.",
    "Кабинет 121": "Кабинет информатики.<br> Здесь изучают языки программирования.",
    "Кабинет 221": "Кабинет начальных классов.",
    "Кабинет 222": "Кабинет начальных классов.",
    "Кабинет 223": "Кабинет начальных классов.",
    "Кабинет 224": "Кабинет начальных классов.",
    "Кабинет 225": "Кабинет начальных классов.",
    "Кабинет 226": "Кабинет информатики.<br> Здесь изучают языки программирования.",
    "Кабинет 227": "Кабинет английского.<br> Здесь изучают английский язык.",
    "Кабинет 231": "Кабинет начальных классов.",
    "Кабинет 232": "Кабинет начальных классов.",
    "Кабинет 233": "Кабинет начальных классов.",
    "Кабинет 234": "Кабинет начальных классов.",
    "Кабинет 235": "Кабинет начальных классов.",
    "Кабинет 236": "Кабинет начальных классов.",
    "Кабинет 138": "Кабинет истории.<br> Здесь изучают историю России и мира.",
    "Кабинет 137": "Кабинет физики.<br> Здесь изучают явления и проводят лаборатнорные работы.",
    "Кабинет 136": "Кабинет химии.<br> Здесь изучают химические реакции.",
    "Кабинет 135": "Кабинет русского языка и литературы.<br> Здесь изучают грамматику и пунктуацию.",
    "Кабинет 134": "Кабинет математики.<br> Здесь изучают алгебру, геометрию и вероятности.",
    "Кабинет 133": "Кабинет русского языка и литературы.<br> Здесь изучают грамматику и пунктуацию.",
    "Кабинет 132": "Кабинет русского языка и литературы.<br> Здесь изучают грамматику и пунктуацию.",
    "Кабинет 131": "Кабинет ИЗО/Черчения.<br> Здесь рисуют и строят схемы.",
    "Большой зал": "Спортивный зал для уроков физической культуры.",
    "Малый зал": "Спортивный зал для уроков физической культуры.",
    "Столовая": "Помещения для приёма пищи.",
    "Кабинет Психолога": "Кабинет, где можно рассказать о своих проблемах.",
    "Актовый зал": "Зал, где проводят общественные мероприятия для всей школы.",
    "Библиотека": "Помещение, где можно взять книгу или учебник для ознакомления."
};

const map = new ol.Map({
    target: 'map',
    layers: [],
    view: new ol.View({ extent: [-500, 0, 1500, 1500], zoom: 0.1, center: [750, 750] })
});

const floors = {
    "1": new ol.layer.Image({ source: new ol.source.ImageStatic({ url: first_floor, imageExtent: [0, 0, 1000, 1000] }) }),
    "2": new ol.layer.Image({ source: new ol.source.ImageStatic({ url: second_floor, imageExtent: [0, 0, 1000, 1000] }) }),
    "3": new ol.layer.Image({ source: new ol.source.ImageStatic({ url: third_floor, imageExtent: [0, 0, 1000, 1000] }) })
};


map.addLayer(floors["1"]);

function createMarker(coord, text) {
    let feature = new ol.Feature({
        geometry: new ol.geom.Point(coord),
        text: text
    });

    feature.setStyle(new ol.style.Style({
        image: new ol.style.Circle({
            radius: 6,
            fill: new ol.style.Fill({ color: 'red' })
        }),
        text: new ol.style.Text({
            text: text,
            offsetY: -12,
            fill: new ol.style.Fill({ color: 'black' }),
            font: '12px Arial'
        })
    }));

    return feature;
}

const markers = {
    "1": new ol.layer.Vector({
        source: new ol.source.Vector({
            features: [
                createMarker([400, 745], "Cтоловая"),
                createMarker([280, 750], "Большой зал"),
                createMarker([213, 278], "Малый зал"),
                createMarker([214, 224], "Кабинет 113"),
                createMarker([731, 744], "Кабинет Психолога"),
                createMarker([731, 414], "Кабинет 212"),
                createMarker([731, 576], "Кабинет 211")
            ]
        })
    }),
    "2": new ol.layer.Vector({
        source: new ol.source.Vector({
            features: [
                createMarker([311, 800], "Библиотека"),
                createMarker([408, 745], "Актовый зал"),
                createMarker([731, 295], "Кабинет 121"),
                createMarker([693, 224], "Кабинет 122"),
                createMarker([584, 224], "Кабинет 123"),
                createMarker([476, 224], "Кабинет 124"),
                createMarker([373, 224], "Кабинет 125"),
                createMarker([292, 224], "Кабинет 126"),
                createMarker([211, 224], "Кабинет 127"),
                createMarker([210, 274], "Кабинет 128"),
                createMarker([731, 386], "Кабинет 226"),
                createMarker([731, 465], "Кабинет 225"),
                createMarker([731, 530], "Кабинет 224"),
                createMarker([731, 602], "Кабинет 223"),
                createMarker([731, 666], "Кабинет 222"),
                createMarker([731, 727], "Кабинет 221"),
                createMarker([636, 473], "Кабинет 227")
            ]
        })
    }),
    "3": new ol.layer.Vector({
        source: new ol.source.Vector({
            features: [
                createMarker([731, 295], "Кабинет 131"),
                createMarker([693, 224], "Кабинет 132"),
                createMarker([584, 224], "Кабинет 133"),
                createMarker([476, 224], "Кабинет 134"),
                createMarker([373, 224], "Кабинет 135"),
                createMarker([292, 224], "Кабинет 136"),
                createMarker([211, 224], "Кабинет 137"),
                createMarker([210, 274], "Кабинет 138"),
                createMarker([731, 386], "Кабинет 236"),
                createMarker([731, 465], "Кабинет 235"),
                createMarker([731, 530], "Кабинет 234"),
                createMarker([731, 602], "Кабинет 233"),
                createMarker([731, 666], "Кабинет 232"),
                createMarker([731, 727], "Кабинет 231"),
            ]
        })  
    })
};

map.addLayer(markers["1"]);
const popup = document.getElementById("popup");
const popupContent = document.getElementById("popup-content");

map.on('click', function(event) {
    let feature = map.forEachFeatureAtPixel(event.pixel, function(feature) {
        return feature;
    });

    if (feature) {
        let coords = feature.getGeometry().getCoordinates();
        let text =  roomsInfo[feature.get('text')] || "Информация о кабинете отсутствует.";

        // Устанавливаем позицию и текст всплывающего окна
        popup.style.left = `${event.pixel[0] + 10}px`;
        popup.style.top = `${event.pixel[1] - 20}px`;
        popupContent.innerHTML = text;
        popup.style.display = "block";
    } else {
        popup.style.display = "none";
    }
});

document.getElementById("floorSelect").addEventListener("change", function() {
    let floor = this.value;
    map.getLayers().clear();
    map.addLayer(floors[floor]);
    map.addLayer(markers[floor]);
    popup.style.display = "none";
});