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
        show_chart(response['sources'], query);
      }
    })
  }
})


function show_chart(sources, query) {

  var sources_sorted = [];

  for (const [source_id, count] of Object.entries(sources)) {
    sources_sorted.push([source_id, count]);
  }

  // sort data
  sources_sorted.sort(function(a,b) {return b[1] - a[1]});

  var source_ids = sources_sorted.map(i => i[0]);
  var num_accounts = sources_sorted.map(i => i[1]);

  $('#main-content').html('<canvas id="query-stats" class="credshed-chart", height="600", width="1000"></canvas>');

  var ctx = document.getElementById('query-stats').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: source_ids,
      datasets: [{
        label: `Accounts by Leak`,
        data: num_accounts,
          backgroundColor: 'rgba(255,255,255,.1)',
          borderColor: get_rainbow_steps(source_ids.length),
        borderWidth: 5
      }]
    },
    options: {
      responsive: false,
      legend: {
        labels: {
          fontColor: "white",
          fontSize: 18
        }
      },
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Accounts',
            fontColor: "white",
            fontSize: 18,
          },
          ticks: {
            beginAtZero: true,
            fontColor: "white",
          }
        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Leaks',
            fontColor: "white",
            fontSize: 18,
          },
          ticks: {
            beginAtZero: true,
            fontColor: "white",
          }
        }]
      }
    }
  });
}