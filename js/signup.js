$('#signup').submit(function() {
    if ($('input[name="password"]').val() != $('input[name=password1]').val()) {
	$('input[name="password1"]').addClass('missmatch');
	$
    } else {
	$('input["name="password1"]').removeClass('missmatch');
    }
    return false;
});

