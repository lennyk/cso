$(document).ready(function () {
    var $name = $('#cc-name');
    var $number = $('#cc-number');
    var $expiration = $('#cc-exp');
    var $cvc = $('#cc-cvc');
    var $icons = $('#cc-icons');

    $('#cso-ticket-form').submit(function (event) {
        var $form = $(this);
        var $submit = $form.find('[type="submit"]');
        var submitInitialText = $submit.val();

        $submit.attr('disabled', true).val('Processing...');
        event.preventDefault();

        // reset errors
        $form.find('.has-error').removeClass('has-error');


        if ($.trim($name.val()).length == 0) {
            // client side validation
            $name.closest('.form-group').addClass('has-error');
        } else {
            // post to server
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
                        //$form.find('.stripe-errors').text(response.error.message).show();
                        $submit.attr('disabled', false).val(submitInitialText);
                        switch (response.error.param) {
                            case 'number':
                                $number.closest('.form-group').addClass('has-error');
                                break;
                            case 'exp_month':
                            case 'exp_year':
                                $expiration.closest('.form-group').addClass('has-error');
                                break;
                            case 'cvc':
                                $cvc.closest('.form-group').addClass('has-error');
                                break;
                        }
                    } else {
                        var token = response.id;
                        $form.append($('<input type="hidden" name="stripe_token" />').val(token));
                        $form.get(0).submit();
                    }

                }
            );
        }
    });

    (function () {
        $number.payment('formatCardNumber');
        $expiration.payment('formatCardExpiry');
        $cvc.payment('formatCardCVC');

        $number.bind('input', function(){
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