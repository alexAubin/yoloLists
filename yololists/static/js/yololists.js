$('#modal-subscribe').on('show.bs.modal', function (event) {
	// Button that triggered the modal
    var button = $(event.relatedTarget)

	// Extract info from data-* attributes
    var list_name = button.data('list-name')
    var list_display_name = button.data('list-display-name')

    // Update the modal's content.
    var modal = $(this)
    modal.find('.modal-subscribe-list-name').text(list_name)
    modal.find('.modal-subscribe-list-display-name').text(list_display_name)
})
