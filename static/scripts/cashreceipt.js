$(document).ready(function () {
    function get_invoices() {
        console.log('working')
        var url = $("#customer-id").data('inquiry-url');
        var customerId = document.getElementById("customer-id").innerText;

        $.ajax({
            url: url,
            data: {'customer': customerId},
            success: function (data) {
                $("#related_invoice").html(data);
            }
        });
    };
    window.onload = get_invoices();

    function add_item() {
        console.log('jumping');
        console.log($('#related_invoice').val());
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        if ($('#related_invoice').val() == '') {
            var ivoice = 0
        } else {
            var invoice = $('#related_invoice').val()
        }

        $.ajax({
            url: $("#add_item").data('url'),
            headers: {'X-CSRFToken': csrftoken},
            type: 'POST',
            data: {
                invoice: invoice,
                description: $('#receipt_description').val(),
                amount: $('#receipt_amount').val()
            },
            success: function (json) {
                document.getElementById("document-form").reset();
                console.log(json);
                console.log('success')
            }
        });
    };

    $('#document-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        add_item();
    });
});
