(function($) {
  var dropZone = document.getElementById('drop-zone');

  var startUpload = function(file) {
    // Upload file to /upload

    $.ajax({
      "url": "/upload",
      "type": "POST",
      "enctype": "multipart/form-data"
    });

  };
})(jQuery);
