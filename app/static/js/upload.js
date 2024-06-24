document.addEventListener('DOMContentLoaded', function () {
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
        var initialMessage = 'Configuration upload initiated...<br>Waiting for completion...';
        toastrElement = toastr.info(initialMessage, 'Info');
        var timeLeft = 30;

        timerInterval = setInterval(function () {
            if (timeLeft > 0) {
                toastrElement.find('.toast-message').html('Configuration upload initiated...<br>Waiting for completion... ' + timeLeft + ' seconds...');
                timeLeft--;
            } else {
                clearInterval(timerInterval);
                // Remove the toast only if the upload is not completed
                if (!xhrCompleted) {
                    toastr.clear(toastrElement);
                }
            }
        }, 1000);
    }

    var xhrCompleted = false;

    document.getElementById('UploadButton').addEventListener('click', function () {
        showInitialToast();

        var xhr = new XMLHttpRequest();
        var url = '/upload_config';

        xhr.open('POST', url, true);

        // Обработчик загрузки
        xhr.onload = function () {
            clearInterval(timerInterval);
            xhrCompleted = true;
            toastr.clear(toastrElement);

            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.status === 'success') {
                    toastr.success('Configuration uploaded successfully.', 'Success', {timeOut: 5000});
                } else {
                    toastr.error('Failed to upload configuration: ' + response.message, 'Error', {timeOut: 5000});
                }
            } else {
                toastr.error('Request failed. Status: ' + xhr.status, 'Error', {timeOut: 5000});
            }
        };

        // Обработчик ошибки
        xhr.onerror = function () {
            clearInterval(timerInterval);
            xhrCompleted = true;
            toastr.clear(toastrElement);
            toastr.error('Request failed. Please check your network connection.', 'Error', {timeOut: 5000});
        };

        xhr.send();
    });
});
