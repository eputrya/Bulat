$(document).ready(function () {
    toastr.options = {
        "positionClass": "toast-middle-center",
        "closeButton": true,
        "progressBar": true,
        "newestOnTop": false
    };

    $('#showConfigButton').on('click', function () {
        $.ajax({
            url: '/show_running_config',
            method: 'POST',
            success: function (response) {
                if (response.status === 'success') {
                    showCustomToastr(response.config);
                } else {
                    toastr.error(response.message, 'Error');
                }
            },
            error: function (response) {
                toastr.error(response.responseJSON.message, 'Error');
            }
        });
    });

    function showCustomToastr(config) {
        var $toast = $('<div class="custom-toast"></div>');
        $toast.append('<div class="toast-body">' + config + '</div>');

        toastr.info($toast, '', { timeOut: 1000 });
    }
});
