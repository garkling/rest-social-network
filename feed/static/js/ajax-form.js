function replaceDocument(docString) {
	const doc = document.open("text/html");
	doc.write(docString);
	doc.close();
}


function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function sameOrigin(url) {
  // test that a given url is a same-origin URL
  // url could be relative or scheme relative or absolute
	const host = document.location.host; // host + port
	const protocol = document.location.protocol;
	const sr_origin = '//' + host;
	const origin = protocol + sr_origin;

	// Allow absolute or scheme relative URLs to same origin
  return (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
    (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') ||
    // or any other URL that isn't scheme relative or absolute i.e relative.
    !(/^(\/\/|http:|https:).*/.test(url));
}


function doAjaxSubmit(e) {
	const form = $(this);
	const btn = $(this.clk);
	let method = btn.data('method') || form.data('method') || form.attr('method') || 'GET';
	method = method.toUpperCase()
	if (method === 'GET') {
		// GET requests can always use standard form submits.
		return;
	}

	let contentType =
		form.find('input[data-override="content-type"]').val() ||
		form.find('select[data-override="content-type"] option:selected').text();
	if (method === 'POST' && !contentType) {
		// POST requests can use standard form submits, unless we have
		// overridden the content type.
		return;
	}

	// At this point we need to make an AJAX form submission.
	e.preventDefault();

	const url = form.attr('action');
	let data;
	if (contentType) {
		data = form.find('[data-override="content"]').val() || ''
	} else {
		contentType = form.attr('enctype') || form.attr('encoding')
		if (contentType === 'multipart/form-data') {
			if (!window.FormData) {
				alert('Your browser does not support AJAX multipart form submissions');
				return;
			}
			// Use the FormData API and allow the content type to be set automatically,
			// so it includes the boundary string.
			// See https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
			contentType = false;
			data = new FormData(form[0]);
		} else {
			contentType = 'application/x-www-form-urlencoded; charset=UTF-8'
			data = form.serialize();
		}
	}

	let ret = $.ajax({
		url: url,
		method: method,
		data: data,
		contentType: contentType,
		processData: false,
		beforeSend: function (xhr, settings) {
			if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
				xhr.setRequestHeader(window.drf.csrfHeaderName, window.drf.csrfToken);
			}
		}
	});

	ret.done(function (data, textStatus, jqXHR) {
		switch (textStatus) {
			case 'nocontent':
				window.location = mainUrl;
				break
			case 'success':
				window.location = document.referrer;
				break
		}
	});
	ret.fail( function (data) {
		const errors = data.responseJSON

		for (let inputName in errors) {
			let errMsg = errors[inputName][0]
			const inputEl = $(`[name=${inputName}]`)
			const helperEl = document.createElement('div')
			// $(inputEl).addClass('is-invalid')
			$(inputEl).after(helperEl)
			$(helperEl).addClass('invalid-tooltip').html(errMsg)
			console.log(inputName, errMsg)
		}

	})

	return ret;
}


function captureSubmittingElement(e) {
	const target = e.target;
	const form = this;
	form.clk = target;
}


$.fn.ajaxForm = function () {
	const options = {}
	return this
		.unbind('submit.form-plugin  click.form-plugin')
		.bind('submit.form-plugin', options, doAjaxSubmit)
		.bind('click.form-plugin', options, captureSubmittingElement);
};


const mainUrl = '/posts/'
