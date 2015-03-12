$(document).ready(function () {
    (function () {
        var selectYear = $(".card-expiry-year"), year = new Date().getFullYear();
        for (var i = 0; i < 12; i++) {
            selectYear.append($("<option value='" + (i + year) + "' " + (i === 0 ? "selected" : "") + ">" + (i + year) + "</option>"))
        }
    })();

    var stripeResponseHandler = function (status, response) {
        var $form = $('#cso-ticket-form');
        $form.find('.has-error').removeClass('has-error');

        if (response.error) {
            $form.find('[data-stripe="' + response.error.param.replace(/_/g, '-') + '"]').closest('.form-group').addClass('has-error');
            $form.find('[type="submit"]').prop('disabled', false);
        } else {
            var token = response.id;
            $form.append($('<input type="hidden" name="stripe_token" />').val(token));
            $form.get(0).submit();
        }
    };

    $('#cso-ticket-form').submit(function (event) {
        var $form = $(this);
        $form.find('[type="submit"]').prop('disabled', true);
        Stripe.card.createToken($form, stripeResponseHandler);
        return false;
    });
});