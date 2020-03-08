$(document).ready(function() {

  loading();

  var urlParams = new URLSearchParams(window.location.search);
  var source_id = urlParams.get('id');

  if (source_id) {

    $.get({
      url: base_api_url + `/source/${source_id}`,
      success: function(response) {
        var source = response['report'];
        stop_loading();
        // top domains
        show_pie(`Domains in ${source['name']}`, source['top_domains']);
        // top password base words
        show_bar(
          `Password base words`,
          source['top_password_basewords'],
          'Base Words',
          'Count'
        );
        // top misc base words
        show_bar(
          `Misc base words`,
          source['top_misc_basewords'],
          'Base Words',
          'Count'
        );
      },
      error: function(response) {
        stop_loading('Failed to fetch stats', error=true);
      }
    })

  } else {
    stop_loading('No source ID specified', error=true);
  }
})