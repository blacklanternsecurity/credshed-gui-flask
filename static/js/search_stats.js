$(document).ready(function() {

  loading();

  var urlParams = new URLSearchParams(window.location.search);
  var query = urlParams.get('query');
  var limit = urlParams.get('limit');
  if (!(limit)) {
    var limit = 10;
  }

  if (query) {

    $.post({
      url: base_api_url + '/search_stats',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        'query': query,
        'limit': limit
      }),
      success: function(response) {
        stop_loading();
        show_bar(`Statistics for "${query}"`, response['sources'], 'Leaks', 'Accounts');
        //show_pie(`Statistics for "${query}"`, response['sources']);
      },
      error: function(response) {
        stop_loading(error=true);
      }
    })
  }
})