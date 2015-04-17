/**
 * Created by Таника on 17.04.2015.
 */
ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map("map", {
            center: [56.859852, 62.690396],
            zoom: 10,
            controls: ['geolocationControl', 'searchControl', 'zoomControl']
        }),
        myCollection = new ymaps.GeoObjectCollection({}, {
            preset: 'islands#blueStretchyIcon' //все метки голубые и растягиваются по размеру одержимого
        });
    // Создаем геообъект с типом геометрии "Точка".
    //myGeoObject = new ymaps.GeoObject({
    //    // Описание геометрии.
    //    geometry: {
    //        type: "Point",
    //        coordinates: [56.859852, 62.690396]
    //    },
    //    // Свойства.
    //    properties: {
    //        // Контент метки.
    //        iconContent: 'Я',
    //        hintContent: 'Ла ла ла'
    //    }
    //});
    //myGeoObject2 = new ymaps.GeoObject({
    //    // Описание геометрии.
    //    geometry: {
    //        type: "Point",
    //        coordinates: [56.812038, 62.620396]
    //    },
    //    // Свойства.
    //    properties: {
    //        // Контент метки.
    //        iconContent: 'Паша',
    //        hintContent: 'Ла ла ла'
    //    }
    //});
    var coords = [
        [56.812038, 62.620396], [56.812038, 62.620396], [56.822038, 62.620396], [56.812038, 62.630396], [56.822038, 62.630396], [56.832038, 62.620396]
    ]
    var myGeoObjects = [];

for (var i = 0; i<coords.length; i++) {
  myGeoObjects[i] = (new ymaps.Placemark(coords[i]));
    myCollection.add(myGeoObjects[i]);
}


    var myClusterer = new ymaps.Clusterer();
    myClusterer.add(myGeoObjects);
    myMap.geoObjects.add(myClusterer);

    //myCollection.add(myGeoObject);
    //myCollection.add(myGeoObject2);
    myMap.geoObjects.add(myCollection);
    //.add(new ymaps.Placemark([55.684758, 37.738521], {
    //    balloonContent: 'цвет <strong>воды пляжа бонди</strong>'
    //}, {
    //    preset: 'islands#icon',
    //    iconColor: '#0095b6'
    //}))
    //.add(new ymaps.Placemark([55.833436, 37.715175], {
    //    balloonContent: '<strong>серобуромалиновый</strong> цвет'
    //}, {
    //    preset: 'islands#dotIcon',
    //    iconColor: '#735184'
    //}))
    //.add(new ymaps.Placemark([55.687086, 37.529789], {
    //    balloonContent: 'цвет <strong>влюбленной жабы</strong>'
    //}, {
    //    preset: 'islands#circleIcon',
    //    iconColor: '#3caa3c'
    //}))
    //.add(new ymaps.Placemark([55.782392, 37.614924], {
    //    balloonContent: 'цвет <strong>детской неожиданности</strong>'
    //}, {
    //    preset: 'islands#circleDotIcon',
    //    iconColor: 'yellow'
    //}))
    //.add(new ymaps.Placemark([55.642063, 37.656123], {
    //    balloonContent: 'цвет <strong>бисмарк-фуриозо</strong>'
    //}, {
    //    preset: 'islands#icon',
    //    iconColor: '#a5260a'
    //}))
    //.add(new ymaps.Placemark([55.826479, 37.487208], {
    //    balloonContent: 'цвет <strong>фэйсбука</strong>'
    //}, {
    //    preset: 'islands#dotIcon',
    //    iconColor: '#3b5998'
    //}))
    //.add(new ymaps.Placemark([55.694843, 37.435023], {
    //    balloonContent: 'цвет <strong>вконтакте</strong>'
    //}, {
    //    preset: 'islands#circleIcon',
    //    iconColor: '#4d7198'
    //}))
    //.add(new ymaps.Placemark([55.790139, 37.814052], {
    //    balloonContent: 'цвет <strong>твиттера</strong>'
    //}, {
    //    preset: 'islands#circleDotIcon',
    //    iconColor: '#1faee9'
    //}));
}

