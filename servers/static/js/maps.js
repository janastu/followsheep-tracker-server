window.App = window.App || {};
(function(L, App) {
    App.map = new L.map("map").setView([12.9791703, 77.5912429], 13);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(App.map);
    App.mapIcon = new L.Icon({
        iconUrl: '/static/images/leaf-green.png',
        iconAnchor: [13, 30],
        iconSize: [25, 41],
        popupAnchor:[-2, -20],
        shadowSize: [41, 41]
    });
    L.marker([512.9791, 77.59124], {icon: App.mapIcon}).addTo(App.map);
  //side menu slide/toggle
  $(".menu-toggle").click(function(e) {
      e.preventDefault();
      $(".wrapper").toggleClass("active");
  });

  //Poppver trigger one-time onload only
  /*$(function () {
        $('[data-toggle="popover"]').popover('show');
  });*/

  //TODO: Destroy popup on activity start


})(window.L, window.App);
