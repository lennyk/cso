// a hack to remove Facebook redirect junk
if (window.location.hash == '#_=_') {
    // Check if the browser supports history.replaceState.
    if (history.replaceState) {
        // Keep the exact URL up to the hash.
        var cleanHref = window.location.href.split('#')[0];
        // Replace the URL in the address bar without messing with the back button.
        history.replaceState(null, null, cleanHref);
    } else {
        // Well, you're on an old browser, we can get rid of the _=_ but not the #.
        window.location.hash = '';
    }
}

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
