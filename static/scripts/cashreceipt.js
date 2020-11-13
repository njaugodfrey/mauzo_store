$(document).ready(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

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

        $.ajax({
            url: $("#add_item").data('url'),
            headers: {'X-CSRFToken': csrftoken},
            type: 'POST',
            data: {
                invoice: $('#related-invoice').val(),
                description: $('#receipt-description').val(),
                amount: $('#receipt-amount').val()
            },
            success: function (json) {
                document.getElementById("document-form").reset();
                console.log(json);
                $("#document-items").prepend(
                    "<tr>",
                    "<td>"+json.invoice+"</td>",
                    "<td>"+json.description+"</td>",
                    "<td>"+json.amount+"</td>",
                    "<a class='item-remove' data-url='{% url 'inventory:remove-item' slug=receipt.slug pk=receipt.id item_pk=item.pk %}' id='delete-post-"+json.item_id+"'>",
                        "<button type='button' class='btn btn-danger'>Remove</button>",
                    "</a>",
                    "</tr>"
                );
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    $('#document-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        add_item();
    });

    function cancel_item(item_primary_key) {
        const csrftoken = getCookie('csrftoken')
        if (confirm('Are you sure you want to remove this item?')==true){
            console.log($(".item-remove").data('url'));

            $.ajax({
                url: $(".item-remove").data('url'),
                headers: {'X-CSRFToken': csrftoken},
                type : "DELETE",
                data : { item_pk : item_primary_key },
                success: function (json) {
                    console.log('Item removed successfully');
                    $('#remove-item-' + item_primary_key).parents("tr").remove(); // hide the item on success
                },
                error : function(xhr,errmsg,err) {
                    // Show an error
                    $('#results').html("<div class='alert-box alert radius' data-alert>"+
                    "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        };
    };
    $("#document-items").on('click', 'a[id^=remove-item-]', function(){
        var item_primary_key = $(this).attr('id').split('-')[2];
        console.log(item_primary_key) // sanity check
        cancel_item(item_primary_key);
    });
});
