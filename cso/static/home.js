// smooth scrolling
$("a[href*='#']").on('click', function (e) {

    if (this.href.split('#')[0] == window.location.href.split('#')[0]) {

        // prevent default anchor click behavior
        e.preventDefault();

        // store hash
        var hash = this.hash;

        var distance = $(this.hash).offset().top - $('.parallax :first-child').offset().top;
        var scrollTime = Math.min(Math.abs($(this.hash).offset().top) / 2, 1200);

        // animate
        $('.parallax').animate({
            scrollTop: distance
        }, scrollTime, function () {
            // TODO: re-implement this in a way that doesn't break parallax scrolling
            //window.location.hash = hash;
        });
    }
});