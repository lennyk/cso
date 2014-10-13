function setFormVisibility() {
    if ($('#id_college_affiliated_0').is(':checked')) {
        // not college
        $('#id_college_verification_type').closest('div.form-group').hide();
        $('#id_college_group').closest('div.form-group').hide();
        $('#id_verification_message').closest('div.form-group').hide();
        $('#id_edu_email').closest('div.form-group').hide();
        $('#existing-user-emails').hide();
    } else {
        // is college
        $('#id_college_verification_type').closest('div.form-group').show();
        $('#id_college_group').closest('div.form-group').show();
        if ($('#id_college_verification_type_1').is(':checked')) {
            // email verification
            $('#id_edu_email').closest('div.form-group').show();
            $('#existing-user-emails').show();
            $('#id_verification_message').closest('div.form-group').hide();
        } else if ($('#id_college_verification_type_2').is(':checked')) {
            // message verification
            $('#id_edu_email').closest('div.form-group').hide();
            $('#existing-user-emails').hide();
            $('#id_verification_message').closest('div.form-group').show();
        }
    }
}

function cleanForm() {
    if ($('#id_college_affiliated_0').is(':checked')) {
        // not college
        $('#id_college_verification_type_0').prop("checked", true);
        $('#id_edu_email').val('');
        $('#id_verification_message').val('');
    } else {
        // is college
        if ($('#id_college_verification_type_1').is(':checked')) {
            // email verification
            $('#id_verification_message').val('');
        } else if ($('#id_college_verification_type_2').is(':checked')) {
            // message verification
            $('#id_edu_email').val('');
        }
    }
}

$('#id_college_affiliated_0').click(setFormVisibility);
$('#id_college_affiliated_1').click(setFormVisibility);
$('#id_college_verification_type_1').click(setFormVisibility);
$('#id_college_verification_type_2').click(setFormVisibility);


$(window).load(function() {
    // hide the no-choice select option
    $('#id_college_verification_type_0').closest('div.radio').hide();
    setFormVisibility();
    // show the form (hidden by default via css)
    $('form.registration-form').show();
});

// clean form when clicking button (before browser tries to validate)
$('form.registration-form :submit').click(cleanForm);
// probably redundant but clean form on submit as well
$('form.registration-form').submit(cleanForm);

// submit the form to logout
$('a.email-resend-verification').click(function() {
    $('#email-resend-verification-address').val(
        $(this).closest('tr').children('.email').first().text()
    );
    $('#email-resend-verification-form').submit();
    return false;
});
