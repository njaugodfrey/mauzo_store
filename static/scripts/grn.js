$(document).ready(function () {
    $("#item-name").change(function () {
        var url = $("#document-form").data('units-url');
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

    function add_item() {
        console.log("create post is working!") // sanity check
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
                unit: $('#uom').val()
            },
            // handle a successful post request
            success: function (json) {
                // remove values from the fields
                document.getElementById("document-form").reset();
                 //log returned json
                console.log(json);
                console.log("success");
                $("#document-items").prepend(
                    "<tr>",
                    "<td>"+json.item_name+"</td>",
                    "<td>"+json.item_quantity+"</td>",
                    "<td>"+json.item_price+"</td>",
                    "<td>"+json.total_cost+"</td>",
                    "<a class='item-remove' data-url='{% url 'inventory:remove-item' slug=receipt.slug pk=receipt.id item_pk=item.pk %}' id='delete-post-"+json.item_id+"'>",
                        "<button type='button' class='btn btn-danger'>Remove</button>",
                    "</a>",
                    "</tr>"
                );
                $("#receipt-total").html(json.document_total);
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
        if (confirm('are you sure you want to remove this item?')==true) {
            console.log($(".item-remove").data('url'));
            $.ajax({
                url : $(".item-remove").data('url'),
                headers: {'X-CSRFToken': csrftoken},// manually send csrftoken
                type : "DELETE",
                // data sent with the delete request
                data : { item_pk : item_primary_key },
                success : function(json) {
                    // update total
                    $("#receipt-total").html(json.receipt_total);
                    // hide the post
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
    $("#document-items").on('click', 'a[id^=remove-item-]', function(){
        var item_primary_key = $(this).attr('id').split('-')[2];
        console.log(item_primary_key) // sanity check
        remove_item(item_primary_key);
    });


    $('#document-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        add_item();
    });
})
