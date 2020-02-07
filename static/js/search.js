$(document).ready(function() {

  prefill_search();

  $('#credshed-search').click(function(e) {
    submit_search();
  })

  $('#search-input').on("keypress", function(e) {
    /* ENTER PRESSED*/
    if (e.keyCode == 13) {
      e.preventDefault();
      submit_search();
    }
  })

  $('#csv-download').click(function() {
    var query = get_search();
    window.open(base_api_url + '/export_csv/' + encodeURIComponent(query), '_blank');
  })

  $('#search-stats').click(function() {
    var query = get_search();
    var params = new URLSearchParams({
      'query': query,
      'limit': 10
    });
    window.open('/search_stats?' + params.toString(), '_blank');
  })
})

function submit_search() {

  $('#results-count').text(` [calculating ...]`);

  // search results
  var query_json = JSON.stringify({
    'query': $('#search-input').val()
  })

  $('#results-container').show()
  $.post({
    url: base_api_url + '/search',
    dataType: 'json',
    contentType: 'application/json',
    data: query_json,
    'success': function(data) {
      save_search();
      prefill_search();
      fill_search_report(data['stats']);
      fill_results(data['accounts']);
      hide_empty_columns();
      $(document).trigger('search-event');

      // result count
      $.post({
        url: base_api_url + '/count',
        data: query_json,
        dataType: 'json',
        contentType: 'application/json',
        success: function(data) {
          var count = data["count"].toLocaleString();
          $('#results-count').text(` [${count} records]`);
        },
      })

    },
    'error': function(data) {
      fill_results([]);
      $('#search-report').addClass('text-danger');
      if (data.responseJSON.error) {
        fill_search_report(data.responseJSON.search_report);
      } else {
        fill_search_report(['Unknown error']);
      }
      $('#search-input').select();
    }
  })
}

function prefill_search() {
  var last_search = get_search();
  if (last_search) {
    $('#search-input').val(last_search);
    $('#search-input').select();
  }
}

function save_search() {
  var query = $('#search-input').val();
  if (query) {
    window.localStorage.setItem('credshed_last_search', query);
  }
}

function get_search() {
  return window.localStorage.getItem('credshed_last_search');
}

function get_search_json() {
  return JSON.stringify({'query': get_search()});
}

function fill_search_report(stats) {

  var report = [];
  report.push(`Searching by ${stats['query_type']}`);
  if (stats['limit'] == stats['count']) {
    report.push(`Showing top ${stats['limit']} results for "${stats['query']}"`);  
  } else {
    report.push(`${stats['count']} results for "${stats['query']}"`);
  }
  report.push(`Searched ${stats['searched']} accounts in ${stats['elapsed']} seconds`)

  var search_report_ul = $('#search-report > ul');
  search_report_ul.empty();
  search_report_ul.removeClass('text-danger');

  for (var i = 0; i < report.length; i++) {
    // Create the list item:
    var item_el = document.createElement('li');
    var item_text = report[i];
    if (item_text.includes('Showing top ')) {
      item_el.classList.add('text-warning');
    }
    // Set its contents:
    item_el.appendChild(document.createTextNode(report[i]));
    // Add it to the list:
    search_report_ul.append(item_el);
  }
}

function fill_results(accounts) {

  // clear last results
  $('#accounts-table > tbody').empty();

  for (var i = 0; i < accounts.length; i++) {
    var account_id = accounts[i]['i'];
    var email = accounts[i]['e'];
    var username = accounts[i]['u'];
    var password = accounts[i]['p'];
    var hash = accounts[i]['h'];
    var misc = accounts[i]['m'];

    $('#accounts-table > tbody:last-child').append(
      `<tr id="${encodeURIComponent(account_id)}"><td title="Details" class="meta-fetch">[i]</td><td>${email}</td><td>${username}</td><td>${password}</td><td>${hash}</td><td>${misc}</td></tr>`
    );
  }
}