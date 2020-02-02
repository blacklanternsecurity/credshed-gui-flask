$(document).ready(function() {

  $('#account-details-close').click(function() {
    $('#account-details').hide();
  })

  $('.draggable').draggable({ cancel: "#account-details-content" });

  $(document).on('search-event', function() {
    $('.meta-fetch').click(function() {
      get_account_metadata(this);
    });
  })

})

function save_account_metadata(account_id, metadata) {
  window.sessionStorage.setItem(`a_${account_id}`, JSON.stringify(metadata));
}

function get_account_metadata(element) {
  var account_id = $(element).closest('tr').attr('id');
  var sources = JSON.parse(window.sessionStorage.getItem(`a_${account_id}`));
  if (sources === null) {
    $.post({
      url: base_api_url + '/metadata/' + encodeURIComponent(account_id),
      success: function(fresh_sources) {
        show_account_details(account_id, fresh_sources, element); 
      }
    })
  } else {
    show_account_details(account_id, sources, element);
  }
}

function show_account_details(account_id, sources, element) {
  save_account_metadata(account_id, sources);
  $('#account-details-content').text('Loading...');
  $('#account-details').show();
  // position window next to clicked element
  var position = $(element).offset();
  position['top'] += 50;
  position['left'] += 50;
  $('#account-details').css(position);
  $('#account-details-content').html(build_account_details(sources));
}

function build_account_details(sources) {
  // create the unordered list
  var ul = document.createElement('ul');
  for (const [source_id, source_name] of Object.entries(sources)) {
    // for (var i = 0; i < sources.length; i++) {
    // Create the link
    var item_a = document.createElement('a');
    item_a.setAttribute('href', `/source_stats?id=${source_id}`);
    // Create the list item:
    var item_el = document.createElement('li');
    var item_text = document.createTextNode(source_name);
    // Set its contents:
    item_el.appendChild(item_a);
    item_a.appendChild(item_text);
    // Add it to the list:
    ul.appendChild(item_el);
  }
  return ul;
}