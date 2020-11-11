$(document).ready(function () {
    function get_invoices() {
        console.log('working')
        var url = $("#customer-id").data('inquiry-url');
        var customerId = document.getElementById("customer-id").innerText;
        console.log(customerId)

        $.ajax({
            url: url,
            data: {'customer': customerId},
            success: function (data) {
                $("#related_invoice").html(data);
                console.log(data)
            }
        });
    };
    window.onload = get_invoices();
});
