$(document).ready(function () {
    toastr.options = {
        "positionClass": "toast-top-right",
        "timeOut": "0",
        "extendedTimeOut": "0",
        "closeButton": true,
        "progressBar": true
    };

    $('#StartTestButton').on('click', function () {
        $.ajax({
            url: '/start',
            type: 'POST',
            success: function (response) {
                if (response.status === 'success') {
                    toastr.success('Test started successfully!');
                    console.log(response.nodes_summary);
                } else {
                    toastr.error('Failed to start test: ' + response.message);
                }
            },
            error: function (xhr, status, error) {
                toastr.error('Error occurred: ' + xhr.responseText);
            }
        });
    });
});