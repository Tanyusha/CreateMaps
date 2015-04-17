/**
 * Created by Таника on 17.04.2015.
 */
ymaps.ready(init);


function init() {
    //var myMap = new ymaps.Map("map", {
    //        center: [56.859852, 62.690396],
    //        zoom: 10,
    //        controls: ['geolocationControl', 'searchControl', 'zoomControl']
    //    }),
    //    myCollection = new ymaps.GeoObjectCollection({}, {
    //        preset: 'islands#blueStretchyIcon' //все метки голубые и растягиваются по размеру одержимого
    //    });
    //var coords = [
    //    [56.812038, 62.620396], [56.812038, 62.620396], [56.822038, 62.620396], [56.812038, 62.630396], [56.822038, 62.630396], [56.832038, 62.620396]
    //]
    //var myGeoObjects = [];
    //
    //for (var i = 0; i < coords.length; i++) {
    //    myGeoObjects[i] = (new ymaps.Placemark(coords[i]));
    //    myCollection.add(myGeoObjects[i]);
    //}
    //
    //
    //var myClusterer = new ymaps.Clusterer();
    //myClusterer.add(myGeoObjects);
    //myMap.geoObjects.add(myClusterer);
    //
    ////myCollection.add(myGeoObject);
    ////myCollection.add(myGeoObject2);
    //myMap.geoObjects.add(myCollection);
}

function addMarks(lots) {
    var myMap = new ymaps.Map("map", {
            center: [56.859852, 62.690396],
            zoom: 10,
            controls: ['geolocationControl', 'searchControl', 'zoomControl','typeSelector']
        }),
        myCollection = new ymaps.GeoObjectCollection({}, {
            preset: 'islands#blueStretchyIcon' //все метки голубые и растягиваются по размеру одержимого
        });
    //var coords = [
    //    [56.812038, 62.620396], [56.812038, 62.620396], [56.822038, 62.620396], [56.812038, 62.630396], [56.822038, 62.630396], [56.832038, 62.620396]
    //]
    var myGeoObjects = [];
    //myGeoObjects[0] = (new ymaps.Placemark(lots[2]['coords']));
    for (var i = 0; i < 60 ; i++) {
        console.log(lots[i]['coords']);
        myGeoObjects[i] = (new ymaps.Placemark(lots[i]['coords']));
        myCollection.add(myGeoObjects[i]);
    }


    var myClusterer = new ymaps.Clusterer();
    myClusterer.add(myGeoObjects);
    myMap.geoObjects.add(myClusterer);

    //myCollection.add(myGeoObject);
    //myCollection.add(myGeoObject2);
    myMap.geoObjects.add(myCollection);
}