$(document).ready(function () {
    var $form = $('#cso-ticket-form');
    var $name = $('#cc-name');
    var $number = $('#cc-number');
    var $expiration = $('#cc-exp');
    var $cvc = $('#cc-cvc');
    var $submit = $('#cc-submit');
    var $icons = $('#cc-icons');

    $form.submit(function (event) {
        event.preventDefault();

        // reset errors
        $form.find('.has-error').removeClass('has-error');

        if ($.trim($name.val()).length == 0) {
            // client side validation
            $name.focus().closest('.form-group').addClass('has-error');
        } else {
            // disable the submit button before contacting Stripe
            $submit.attr('disabled', true);

            // post to Stripe
            var expiration = $expiration.payment('cardExpiryVal');
            Stripe.card.createToken(
                {
                    name: $name.val(),
                    number: $number.val(),
                    cvc: $cvc.val(),
                    exp_month: (expiration.month || 0),
                    exp_year: (expiration.year || 0)
                },
                function (status, response) {
                    if (response.error) {
                        // errors from Stripe
                        $submit.attr('disabled', false);
                        switch (response.error.param) {
                            case 'number':
                                $number.focus().closest('.form-group').addClass('has-error');
                                break;
                            case 'exp_month':
                            case 'exp_year':
                                $expiration.focus().closest('.form-group').addClass('has-error');
                                break;
                            case 'cvc':
                                $cvc.focus().closest('.form-group').addClass('has-error');
                                break;
                        }
                    } else {
                        // success from Stripe, posting to CSO
                        $submit.text('Processing ').append($('<i class="fa fa-spinner fa-spin"></i>'));
                        var token = response.id;
                        $form.append($('<input type="hidden" name="stripe_token" />').val(token));
                        $form.get(0).submit();
                    }
                }
            );
        }
        // Prevent the form from submitting with the default action
        return false;
    });

    (function () {
        $number.payment('formatCardNumber');
        $expiration.payment('formatCardExpiry');
        $cvc.payment('formatCardCVC');

        $number.bind('input', function () {
            $icons.find('.fa').removeClass('text-primary');
            var type = $.payment.cardType($(this).val());
            if (type == 'visa') {
                $('.fa-cc-visa').addClass('text-primary');
            } else if (type == 'mastercard') {
                $('.fa-cc-mastercard').addClass('text-primary');
            } else if (type == 'amex') {
                $('.fa-cc-amex').addClass('text-primary');
            } else if (type == 'discover') {
                $('.fa-cc-discover').addClass('text-primary');
            }
        });
    })();
});