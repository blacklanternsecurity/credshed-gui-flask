

// Given a JSON object, creates a canvas element
// and returns the labels and values for the chart
// Used for both Pie and Bar charts
function prep_chart(json_data, limit=10, div_id=null) {

  var data_sorted = [];

  for (const [label, count] of Object.entries(json_data)) {
    data_sorted.push([label, count]);
  }

  // sort data
  data_sorted.sort(function(a,b) {return b[1] - a[1]});

  var labels = data_sorted.map(i => i[0]).slice(0, limit);
  var counts = data_sorted.map(i => i[1]).slice(0, limit);

  if (div_id == null) {
    num_charts = $('#main-content canvas').length;
    div_id = `chart${num_charts}`;
  }

  $('#main-content').append(`<canvas id="${div_id}" class="credshed-chart", height="600", width="1000"></canvas>`);

  var ctx = document.getElementById(div_id).getContext('2d');

  return [ctx, labels, counts];

}

function show_pie(chart_label, json_data, limit=10, div_id=null) {

  var [ctx, labels, counts] = prep_chart(json_data, limit, div_id)
  var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels.map(i => [i]),
      datasets: [{
        title: chart_label,
        data: counts,
        backgroundColor: get_pie_green(labels.length),
      }]
    },
    options: {
      title: {
        display: true,
        text: chart_label,
        fontColor: "white",
        fontSize: 22,
      },
      responsive: false,
      legend: {
        position: 'bottom',
        align: 'start',
        labels: {
          fontColor: "white",
          fontSize: 18
        }
      },
    }
  });
}


function clear_charts() {

  $('#main-content canvas').remove();

}


function show_bar(chart_label, json_data, key_label, value_label, limit=10, div_id=null) {

  var [ctx, labels, counts] = prep_chart(json_data, limit, div_id);

  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        data: counts,
        backgroundColor: get_bar_green(labels.length),
      }]
    },
    options: {
      title: {
        display: true,
        text: chart_label,
        fontColor: "white",
        fontSize: 22,
      },
      responsive: false,
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: value_label,
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
            labelString: key_label,
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