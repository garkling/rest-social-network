$('#edit-btn, #edit-cancel').click( function toggleFormView (e) {

	$('#post-update-form, #post-content').each( function () {
		$(this).is(':visible') ? $(this).fadeOut() : $(this).fadeIn()
	})
})
