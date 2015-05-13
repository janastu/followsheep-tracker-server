window.App = window.App || {};
(function($, Backbone, _, L, App)
 {
   var tracksView = Backbone.View.extend({
     el: $("#tracks-list"),
     events: {
       "click li": "onTrackClick"
     },
     initialize: function(options) {
       // set the collection and call render
       this.collection = options['collection'];
       this.template = _.template($("#tracks-template").html());
       this.render();
     },
     render: function() {
       _.each(this.collection.models, function(val, key) {
         $(this.el).append(this.template(val.toJSON()));
       }, this);
     },
     onTrackClick: function(event) {
       if(App.map.hasLayer(App.addedTrack)) {
         App.map.removeLayer(App.addedTrack);
       }
       var obj = this.collection.where({'id': $(event.currentTarget).attr('id')});
       var track = obj[0].get('track');
       // the track gets visualized on the map.
       App.addedTrack = L.geoJson(track, {
         style: function(feature) {
           return {color: 'red'};
         },
         onEachFeature: function(feature, layer) {
           switch(feature.properties.name) {
           case 'Picture':
             layer.bindPopup("<img class='img-responsive' src='static/data/extracted_data/" +
                             obj[0].get('device_ID') + '/' + obj[0].get('User') + '/' +
                             feature.properties.link1_href + "'/>");
             break;
           case 'Voice recording':
             layer.bindPopup("<audio controls='controls' src='static/data/extracted_data/" +
                             obj[0].get('device_ID') + '/' + obj[0].get('User') + '/' +
                             feature.properties.link1_href + "'/>");
             break;
           default:
             layer.bindPopup(feature.properties.name);
             break;
           }
         }
       }).addTo(App.map);
       App.map.fitBounds(App.addedTrack.getBounds());
     }
   });

   // A backbone collection to represent set of tracks stored on the server.
   App.Tracks = Backbone.Collection.extend({
     model: Backbone.Model,
     url: '/tracks',
     initialize: function(models) {
       this.add(models);
       this.set({'view': new tracksView({'collection': this})});
     }
   });
 }
)(window.jQuery, window.Backbone, window._, window.L, window.App);
