window.App = window.App || {};
(function(L, App) {
    App.map = new L.map("map").setView([12.9791703, 77.5912429], 13);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(App.map);
  // To add different icons
    App.ColorIcon = L.Icon.extend({
  options: {
	iconAnchor:   [10, 34],
	popupAnchor: [0,-34]
	}
  });

    App.pictureIcon = new App.ColorIcon({iconUrl: '../static/images/picture_icon.png'}),
      audioIcon = new App.ColorIcon({iconUrl: '../static/images/audio_icon.png'}),
      textIcon = new App.ColorIcon({iconUrl: '../static/images/text_icon.png'});


  

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
