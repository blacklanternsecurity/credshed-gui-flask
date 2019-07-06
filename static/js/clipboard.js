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


$('.js-copy-all').click(function() {
  // Initialize
  // ---------------------------------------------------------------------

  // Tooltips
  // Requires Bootstrap 3 for functionality
  $('.js-tooltip').tooltip();

  var text = $( ".credshed-account" )
    .map(function() {
      return this.innerText;
    })
    .get()
    .join('\n');

  // Copy to clipboard

  // replaces break tags with newlines
  // var text = $('#search-results').html().replace(/<br>/g, '\n').trim();
  copyToClipboard(text, $(this));
});


$('.js-copy-one').click(function() {

  $('.js-tooltip').tooltip();

  var text = $(this).find('div')[0].innerText

  copyToClipboard(text, $(this));
});