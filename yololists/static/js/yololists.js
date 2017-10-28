
// When loading the subscribe modal
$('#modal-subscribe').on('show.bs.modal', function (event) {

    $("#modal-subscribe-answer").text("")

    // Button that triggered the modal
    var button = $(event.relatedTarget)

    // Extract info from data-* attributes
    var list_name = button.data('list-name')
    var list_display_name = button.data('list-display-name')

    // Update the modal's content.
    var modal = $(this)
    modal.find('.modal-subscribe-list-name').text(list_name)
    modal.find('.modal-subscribe-list-display-name').text(list_display_name)
    modal.find("[name=list-name]").val(list_name)
});


// When submitting the subscribe modal
$('#modal-subscribe-form').on('submit', function(e){

    e.preventDefault();

    // Set some nice 'loading' effect on the submit button...
    var $submit_button = $("#modal-subscribe-submit");
    $submit_button.button("loading");
    setTimeout(function() {
        $submit_button.button('reset');
    }, 1000);

    // Submit the form
    $.ajax({
        url: "/subscribe",
        type: 'POST',
        data: $('#modal-subscribe-form').serialize(),
        success: function(data) {
            $submit_button.button('reset');
            // Display the answer
            if (data.status == "OK")
            {
                $("#modal-subscribe-answer").addClass("text-success");
                $("#modal-subscribe-answer").removeClass("text-danger");
            }
            else
            {
                $("#modal-subscribe-answer").addClass("text-danger");
                $("#modal-subscribe-answer").removeClass("text-success");
            }
            $("#modal-subscribe-answer").text(data.message);
        }
    });
});

// Simple toggle button/radio code
$('.btn-toggle').click(function() {
    $(this).find('.btn').toggleClass('active');

    if ($(this).find('.btn-primary').length>0) {
        $(this).find('.btn').toggleClass('btn-primary');
    }
    if ($(this).find('.btn-danger').length>0) {
        $(this).find('.btn').toggleClass('btn-danger');
    }
    if ($(this).find('.btn-success').length>0) {
        $(this).find('.btn').toggleClass('btn-success');
    }
    if ($(this).find('.btn-info').length>0) {
        $(this).find('.btn').toggleClass('btn-info');
    }

    $(this).find('.btn').toggleClass('btn-default');

});

$( "#toggle-advanced-member-options" ).click(function() {
    $( ".advanced-member-option" ).toggle();
    $(this).find("a").toggle();
});
