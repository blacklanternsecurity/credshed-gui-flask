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
      data: {
        'query': query,
        'limit': limit
      },
      success: function(response) {
        stop_loading();
        show_bar(`Statistics for "${query}"`, response['report'], 'Leaks', 'Accounts');
        //show_pie(`Statistics for "${query}"`, response['sources']);
      },
      error: function(response) {
        stop_loading(error=true);
      }
    })
  }
})