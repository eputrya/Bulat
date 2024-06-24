$(document).ready(function () {
    toastr.options = {
        "positionClass": "toast-middle-center",
        "closeButton": true,
        "progressBar": true,
        "timeOut": "0",
        "extendedTimeOut": "0"
    };

    var timerInterval;
    var toastrElement;


    function showInitialToast() {
        var initialMessage = 'Configuration upload initiated...<br>Restarting device in 120 seconds...';
        toastrElement = toastr.info(initialMessage, 'Info');
        var timeLeft = 120;


        timerInterval = setInterval(function () {
            if (timeLeft > 0) {
                toastrElement.find('.toast-message').html('Configuration upload initiated...<br>Restarting device in ' + timeLeft + ' seconds...');
                timeLeft--;
            } else {
                clearInterval(timerInterval);
            }
        }, 1000);
    }

    $('#DefaultConfigButton').on('click', function () {
        showInitialToast();
        $.ajax({
            type: 'POST',
            url: '/copy_default_config',
            success: function (response) {
                clearInterval(timerInterval);
                toastrElement.fadeOut();
                if (response.status === 'success') {
                    toastr.success(response.message, 'Success');
                } else {
                    toastr.error('Failed to upload configuration: ' + response.message, 'Error');
                }
            },
            error: function (error) {
                clearInterval(timerInterval);
                toastrElement.fadeOut();
                toastr.error('Request failed. Status: ' + error.status, 'Error');
            }
        });
    });
});
