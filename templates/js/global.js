$.ajaxSetup({
  statusCode: {
    401: function() {
      // redirect to login page on 401
      window.location.href = "/login";
    },
  }
})

base_api_url = "{{ base_api_url }}";


function type_text (target, message, index=0, interval=1) {
  // cut the first line every so often
  if (display_loading == true) {
    if (index % 5 == 0) {
      // break the textblock into an array of lines
      var lines = $(target).text().split('\n');
      // remove one line, starting at the first position
      if (lines.length > 40) {
        lines.splice(0,1);
        // join the array back into a single string
        $(target).text(lines.join('\n'));
      }
    }
    if (index < message.length) {
      $(target).append(message[index++]);
      setTimeout(function () { type_text(target, message, index, interval); }, interval);
    } else {
      // start over if we reach the end
      $(target).empty();
      type_text(target, message, index=0, interval);
    }
  } else {
    return
  }
}

function loading(filename="/static/js/search.js") {
  $('#main-loading').text('Loading ...');
  $('#main-loading').removeAttr('class');
  $('#main-loading').show();
  $('#main-content').html('<pre id="code-scroll"></pre>');
  display_loading = true;
  async_loading(filename);
}

async function async_loading (filename) {
  $.get({
    url: filename,
    success: function (response) {
      type_text('#code-scroll', response);
    }
  })
}

function stop_loading(message='Error', error=false) {
  if (error === true) {
    $('#main-loading').text(message);
    $('#main-loading').addClass('text-danger');
    $('#main-loading').show();
  } else {
    $('#main-loading').hide();
    $('#main-content').empty();
  }
  display_loading = false;
}


function unhide_columns() {
  $('#accounts-table th').show();
  $('#accounts-table td').show();
}


function hide_empty_columns() {
  $('#accounts-table th').each(function(i) {
    var remove = 0;

    var tds = $(this).parents('table').find('tr td:nth-child(' + (i + 1) + ')')
    tds.each(function(j) { if (this.innerHTML == '') remove++; });

    if (remove == ($('#accounts-table tr').length - 1)) {
      $(this).hide();
      tds.hide();
    }
});
}