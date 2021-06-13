const end = '-fill'


function registerRate(obj, pk, user_rate) {
	const likeCountId = `#like-count-${pk}`
	const dislikeCountId = `#dislike-count-${pk}`

	const clickedIcon = $(obj).children()
	const relatedIcon = $(
		$(clickedIcon).attr('id') === likeCountId.replace('#', '') ? dislikeCountId: likeCountId
	);

	$.ajax({
		url: `/posts/rate`,
		type: 'get',
		data: {pk, user_rate}
	}).done(function (data) {
		toggleClickedIcon(clickedIcon, relatedIcon)

		$(likeCountId).html(data['likes']);
		$(dislikeCountId).html(data['dislikes']);

	}).fail(function (err) {
		console.log(err)
	});
}

function toggleClickedIcon(clickedIcon, relatedIcon) {
	let currentIconClass = $(clickedIcon)[0].classList[1];
	let newIconClass;

	if (currentIconClass.endsWith(end)) {
		newIconClass = currentIconClass.replace(end, '');
	} else {
		newIconClass = currentIconClass.concat(end);
	}

	$(clickedIcon).removeClass(currentIconClass).addClass(newIconClass);
	disableRelatedIcon(relatedIcon)
}


function disableRelatedIcon(relatedIcon) {
	let currentIconClass = $(relatedIcon)[0].classList[1];

	if (currentIconClass.endsWith(end)) {
		$(relatedIcon).removeClass(currentIconClass).addClass(currentIconClass.replace(end, ''))
	}

}
