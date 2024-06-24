$(document).ready(function () {
    toastr.options = {
        "positionClass": "toast-middle-center",
        "timeOut": "0",
        "extendedTimeOut": "0",
        "closeButton": true,
        "progressBar": true
    };

    $('#showReportButton').on('click', function () {
        $.ajax({
            url: '/check_report',
            type: 'GET',
            success: function (response) {
                if (response.exists) {
                    window.open('/report_directory/index.html', '_blank');
                } else {
                    toastr.error('Report not found. Please generate a report and try again.');
                }
            },
            error: function () {
                toastr.error('Report not found');
            }
        });
    });
});
