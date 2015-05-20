/**
 * Created by Таника on 19.04.2015.
 */

ymaps.ready(init);
function init() {
    var myMap = new ymaps.Map("map", {
        center: [56.859852, 62.690396],
        zoom: 10,
        controls: ['geolocationControl',  'zoomControl', 'typeSelector']
    });
    //'searchControl',
    var objectManager = new ymaps.ObjectManager({
        // Использовать кластеризацию.
        clusterize: true
    });
    jQuery.getJSON('static/data.json', function (json) {
        console.log(json);
        objectManager.add(json);
    });
    myMap.geoObjects.add(objectManager);
}