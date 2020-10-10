$(document).ready(function () {

    $("#id_product")

    /*
        On submiting the form, send the POST ajax
        request to server and after successfull submission
        display the object.
    */
    $("#receipt-form").submit(function (e) {
        // prevent page from reload and default actions
        e.preventDefault();
        //serialize data to send to form
        var serializedData = $(this).serialize();
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: $("#add_item").data('url'),
            data: serializedData,
            success: function (response) {
                // on successfully creating an object
                // 1. clear the form
                $("#receipt-form").trigger('reset');
                // 2. focus to product input
                $("#id_product").focus();

                // display added item on table
                var obj = JSON.parse(response["obj"]);
                var fields = obj[0]["fields"];
                $("#receipt-items tbody").prepend(
                    `<tr>
                    <td>${fields["product.stock_code"]||""}</td>
                    <td>${fields["product.stock_name"]||""}</td>
                    <td>${fields["quantity"]||""}</td>
                    <td>${fields["price"]||""}</td>
                    <td>${fields["amount"]||""}</td>
                    <td>${fields["product.stock_vat_code"]||""}</td>
                    </tr>`
                )
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            },
        });
    });

    
});