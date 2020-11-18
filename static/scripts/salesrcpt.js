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
    }
    const csrftoken = getCookie('csrftoken');

    $("#item-name").change(function () {
        console.log('working')
        var url = $("#receipt-form").data('units-url');
        var itemId = $(this).val();
        console.log(itemId)

        $.ajax({
            url: url,
            data: {
                'item': itemId
            },
            success: function (data) {
                $("#uom").html(data);
                console.log(data)
            }
        });
    });


    $("#uom").change(function () {
        var url = $("#receipt-form").data('price-url');
        var unitId = $(this).val();
        console.log(unitId)

        $.ajax({
            url: url,
            data: {
                'unit': unitId
            },
            success: function (data) {
                $("#price").html(data);
                console.log(data)
            }
        });
    });

    function add_receipt_items() {
        console.log("create post is working!") // sanity check
        console.log($('#item-name').val());
        console.log($('#item-quantity').val());
        console.log($('#item-price').val());
        console.log($('#uom').val());
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            url: $("#add_item").data('url'),
            headers: {'X-CSRFToken': csrftoken},// manually send csrftoken
            type: 'POST',
            // data sent with the add item form
            data: {
                item: $('#item-name').val(),
                quantity: $('#item-quantity').val(),
                price: $('#item-price').val(),
                uom: $('#uom').val()
            },
            // handle a successful post request
            success: function (json) {
                document.getElementById("receipt-form").reset();
                // remove values from the fields
                $("#item-name").trigger("reset");
                $("#item-quantity").trigger("reset");
                $("uom").trigger("reset");
                $("#item-price").trigger("reset"); 
                //log returned json
                console.log(json);
                console.log("success");
                $("#receipt-items").prepend(
                    "<tr>",
                    "<td>"+json.item_name+"</td>",
                    "<td>"+json.item_quantity+"</td>",
                    "<td>"+json.item_price+"</td>",
                    "<td>"+json.total_cost+"</td>",
                    "<td>"+json.item_vat+"</td>",
                    "<a class='item-remove' data-url='{% url 'inventory:remove-item' slug=receipt.slug pk=receipt.id item_pk=item.pk %}' id='remove-item-"+json.item_id+"'>",
                        "<button type='button' class='btn btn-danger'>Remove</button>",
                    "</a>",
                    "</tr>"
                );

                $("#receipt-total").html(json.receipt_total);
                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    function remove_item(item_primary_key) {
        if (confirm('are you sure you want to remove this item?')==true) {
            console.log($(".item-remove").data('url'));
            $.ajax({
                url : $("#receipt-items").data('url'),
                headers: {'X-CSRFToken': csrftoken},// manually send csrftoken
                type : "DELETE",
                // data sent with the delete request
                data : { item_pk : item_primary_key },
                success : function(json) {
                    // hide the item
                  $('#remove-item-' + item_primary_key).parents("tr").remove(); // hide the item on success
                  console.log("item removal successful");
                },
    
                error : function(xhr,errmsg,err) {
                    // Show an error
                    $('#results').html("<div class='alert-box alert radius' data-alert>"+
                    "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        } else {
            return false
        }
    };

    // Delete post on click
    $("#receipt-items").on('click', 'a[id^=remove-item-]', function(){
        var item_primary_key = $(this).attr('id').split('-')[2];
        console.log(item_primary_key) // sanity check
        remove_item(item_primary_key);
    });


    $('#receipt-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        add_receipt_items();
    });

    // Void receipt/sales returns
    function sales_returns(item_primary_key) {
        console.log("sales return is working!") // sanity check
        $.ajax({
            url: $(".item-return").data('return-url'),
            headers: {'X-CSRFToken': csrftoken},// manually send csrftoken
            type: 'POST',
            data : { item_pk : item_primary_key },
            success: function (json) {
                console.log(json);
                console.log("Success");

                $('#remove-item-' + item_primary_key).parents("tr").remove();

                $("#returned-items-table").prepend(
                    "<tr>",
                    "<td>"+json.item_name+"</td>",
                    "<td>"+json.item_quantity+"</td>",
                    "<td>"+json.item_uom+"</td>",
                    "<td>"+json.item_price+"</td>",
                    "<td>"+json.total_cost+"</td>",
                    "</tr>"
                );
            }
        });
    };

    $("#return-items").on('click', 'a[id^=remove-item-]', function(){
        var item_primary_key = $(this).attr('id').split('-')[2];
        console.log(item_primary_key) // sanity check
        sales_returns(item_primary_key);
    });

    
})
