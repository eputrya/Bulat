$(document).ready(function () {
    $('#connectForm').on('submit', function (event) {
        event.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            method: $(this).attr('method'),
            data: $(this).serialize(),
            success: function (response) {
                toastr.success(response.message, 'Success', {
                    "timeOut": 3000
                });
            },
            error: function (response) {
                toastr.error(response.responseJSON.message, 'Error', {
                    "timeOut": 5000
                });
            }
        });
    });
});
