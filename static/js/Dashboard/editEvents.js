$(document).ready(function () {
    $('#edit-button').on('click', function () {
        $('#view_name').attr('readonly',false);
        console.log("hi")
        $('#view_date').attr('readonly',false);
        $('#view_description').attr('readonly',false);
        $('#view_poster').attr('disabled',false);
        $('#view_registration_fee').attr('readonly',false);
        $('#view_payment_no').attr('readonly',false);
        $('#edit-button').css('display','none');
        $('#submit-button').css('display','block');
    });    
});