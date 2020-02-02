$(document).ready(function() {

  loading();

  var urlParams = new URLSearchParams(window.location.search);
  var source_id = urlParams.get('id');

  if (source_id) {

    $.get({
      url: base_api_url + `/source/${source_id}`,
      dataType: 'json',
      contentType: 'application/json',
      success: function(response) {
        stop_loading();
        show_pie(`Domains in ${response['name']}`, response['top_domains']);
      },
      error: function(response) {
        stop_loading('Failed to fetch stats', error=true);
      }
    })
  } else {
    stop_loading('No source ID specified', error=true);
  }
})