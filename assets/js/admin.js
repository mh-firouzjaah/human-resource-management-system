$(function () {
	$(':input[type="number"]').css('width', '20em');

	// $(':input[type="number"]').bind('keyup', function (e) {
	// 	console.log(e);
	// });

	$(':input[type="number"]').bind(
		'keyup input change click',
		function (e) {
			$(this).attr('type', 'text');
			$(this).val(
				Number(
					$(this)
						.val()
						.replace(/[^\d.-]/g, '')
				).toLocaleString()
			);
		}
	);
	$(':input[type="number"]').bind('click', function (e) {
		$(this).select();
	});

	$(':input[type="number"]').bind('focusout', function (e) {
		$(this).val(
			$(this)
				.val()
				.replace(/[^\d.-]/g, '')
		);
		$(this).attr('type', 'number');
	});
});
