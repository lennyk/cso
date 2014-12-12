// replace login buttons with a spinner when clicked
$('#login-buttons a').click(function () {
    $('#login-buttons').hide();
    $('#login-spinner').show();
});

// submit the form to logout
$('#logout-link').click(function () {
    $(this).parents('form').submit();
    return false;
});

// close navbar collapse on click
$('.navbar a').on('click', function () {
    if ($(this).attr('href') !== '#') {
        var toggle = $('.navbar-toggle');
        if (toggle.is(':visible') && $('.navbar-collapse').is(':visible')) {
            toggle.click();
        }
    }
});

function removeHash() {
    var scrollV, scrollH, loc = window.location;
    if ("pushState" in history)
        history.pushState("", document.title, loc.pathname + loc.search);
    else {
        // Prevent scrolling by storing the page's current scroll offset
        scrollV = document.body.scrollTop;
        scrollH = document.body.scrollLeft;

        loc.hash = "";

        // Restore the scroll offset, should be flicker free
        document.body.scrollTop = scrollV;
        document.body.scrollLeft = scrollH;
    }
}

$(document).ready(function () {
    if (window.location.hash == "#home") {
        removeHash();
    }
});
