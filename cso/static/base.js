// replace login buttons with a spinner when clicked
$('#login-buttons a').click(function() {
    $('#login-buttons').hide();
    $('#login-spinner').show();
});

// submit the form to logout
$('#logout-link').click(function() {
    $(this).parents('form').submit();
    return false;
});

