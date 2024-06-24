$(document).ready(function () {
    $('#showVersionButton').on('click', function () {
        $.ajax({
            url: '/show_version',
            method: 'POST',
            success: function (response) {
                var formattedVersion = response.version.replace(/\n/g, '<br>');
                toastr.success('Version: <br>' + formattedVersion, 'Success', {
                    "timeOut": 3000
                });
            },
            error: function (response) {
                toastr.error(response.responseJSON.message, 'Error');
            }
        });
    });
});
