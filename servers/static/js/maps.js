window.App = window.App || {};
(function(L, App) {
    App.map = new L.map("map").setView([12.9791703, 77.5912429], 13);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(App.map);
  //side menu slide toggle
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
