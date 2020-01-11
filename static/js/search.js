$(document).ready(function() {

    prefill_search();

    $('.meta-fetch').click(function() {

        var target = $(this).attr('data-target')
        var account_id = target.substring(6, target.length)

        if (!$(target).hasClass('meta-fetched')) {
            $.ajax({url: '/metadata/' + account_id, success: function(result) {
                if (result.length > 0) {
                    $(target).html(result);
                    $(target).addClass('meta-fetched');
                };
            }});
        };
    });

    $('#credshed-search').click(function(e) {
        submit_search();
    })

    $('input').on("keypress", function(e) {
        /* ENTER PRESSED*/
        if (e.keyCode == 13) {
            e.preventDefault();
            submit_search();
        }

    })

    $('#csv-download').click(function() {
        console.log('clicked');
        query = get_search();
        window.open('/export_csv?query=' + query, '_blank');
    })
})

function submit_search() {

    var search_form = $('#search-form').serialize();
    $('.results-container').show()
    $.ajax({
        'url': '/search',
        'method': 'POST',
        'data': search_form,
        'success': function(data) {
            save_search();
            prefill_search();
            $('#search-report').removeClass('text-danger');
            $('#search-report').html(data['search_report'].join('<br>'));
            fill_results(data['accounts']);
            $(document).trigger('search-event');
        },
        'error': function(data) {
            if (data.responseJSON.error) {
                $('#search-report').text(data.responseJSON.search_report);
                $('#search-report').addClass('text-danger');
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

function fill_results(accounts) {

    // clear last results
    $('#accounts-table > tbody').empty();

    for (var i = 0; i < accounts.length; i++) {
        var account_id = accounts[i]['i'];
        var email = accounts[i]['e'];
        var username = accounts[i]['u'];
        var password = accounts[i]['p'];
        var misc = accounts[i]['m'];

        $('#accounts-table > tbody:last-child').append(
            `<tr id="${account_id}"><td>${email}</td><td>${username}</td><td>${password}</td><td>${misc}</td></tr>`
        );
    }
}
/*
{% for result in results %}
  <tr>
    <td class="align-top" style="position:absolute">
      <button class="btn btn-sm btn-outline-secondary font-weight-bold meta-fetch text-success bg-light" type="button" data-toggle="collapse" data-target="#meta-{{ result._id }}" aria-expanded="false" aria-controls="meta-{{ result._id }}">
        &gt;
      </button>
    </td>
    <td class="ml-5 js-tooltip js-copy-one" data-toggle="tooltip" title="Copy to clipboard" scope="row">
      <div class="ml-5 my-1 credshed-account text-white font-weight-bold" _id="acc-{{ result._id }}">
        {{ result }}
      </div>
      <div class="ml-5 text-dark collapse" id="meta-{{ result._id }}"><ul><li></li></ul></div>
    </td>
  </tr>
{% endfor %}
*/

/*
  <h6>
    {% for entry in search_report %}
      {% if ' limited to ' in entry %}
        <span class="text-warning">
          <strong>
            {{ entry }}<br>
            Use the CSV download feature if you want everything
          </strong>
        </span>
      {% else %}
        <span>{{ entry }}</span>
      {% endif %}
    <br>
    {% endfor %}
  </h6>
*/