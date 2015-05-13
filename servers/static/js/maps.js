window.App = window.App || {};
(function(L, App) {
  App.map = new L.map("map").setView([51.505, -0.09], 13);
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(App.map);

})(window.L, window.App);
