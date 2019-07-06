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