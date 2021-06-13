(() => {
	$('.form-group > input, .form-group > textarea').keyup( function () {

		let empty = false;

		$('.form-group > input, .form-group > textarea').each( function () {
			if (!$(this).val()) {
				empty = true;
			}
		});

		if (empty) {
			$('#post-button').attr('disabled', 'disabled');
		} else {
			$('#post-button').removeAttr('disabled');
		}

	});

})()
