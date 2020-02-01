$(document).ready(function() {

  $('input').on("keypress", function(e) {
    /* ENTER PRESSED*/
    if (e.keyCode == 13) {
      e.preventDefault();
      $('#login-button').click();
    }
  })

  $('#login-button').click(function(e) {

    $.post({
      url: base_api_url + $('#login-form').attr('action'),
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        'username': $('#login-username').val(),
        'password': $('#login-password').val()
      }),
      success: function(data) {
        console.log('success ' + data);
        window.location.href = '/';
      },
      error: function(data) {
        console.log('error ' + data);
      }
    })
  })

})