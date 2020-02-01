// COPY TO CLIPBOARD
// Attempts to use .execCommand('copy') on a created text field
// Falls back to a selectable alert if not supported
// Attempts to display status in Bootstrap tooltip
// ------------------------------------------------------------------------------

function copyToClipboard(text, el) {
  var copyTest = document.queryCommandSupported('copy');
  var elOriginalText = el.attr('data-original-title');

  if (copyTest === true) {
    var copyTextArea = document.createElement("textarea");
    copyTextArea.value = text;
    document.body.appendChild(copyTextArea);
    copyTextArea.select();
    try {
      var successful = document.execCommand('copy');
      var msg = successful ? 'Copied '.concat(text.length).concat(' bytes') : 'Unable to copy';
      el.attr('data-original-title', msg).tooltip('show');
    } catch (err) {
      console.log('Unable to copy');
    }
    document.body.removeChild(copyTextArea);
    el.attr('data-original-title', elOriginalText);

  } else {
    // Fallback if browser doesn't support .execCommand('copy')
    window.prompt("Copy to clipboard: Ctrl+C or Command+C, Enter", text);
  }
}

function getAccountText(_,el) {
  var text = [];
  $(el).find('td:not(:first)').each(function(k,v) {
    text.push($(v).text());
  })
  return text.join(':');
}

$(document).ready(function() {

  $('.js-copy-all').click(function() {
    $(this).tooltip();
    var text = $('#accounts-table > tbody > tr')
      .map(getAccountText).get().join('\n');
    copyToClipboard(text, $(this));
  });

  $(document).on('search-event', function() {
    $('#accounts-table > tbody > tr > td:not(:first)').click(function() {
      $(this).tooltip();
      copyToClipboard($(this).text(), $(this));
    });
  })

})