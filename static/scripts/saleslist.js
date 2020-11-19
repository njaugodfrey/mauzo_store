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

    function clear(receipt_pk) {
        $.ajax({
            url: $('#receipts-list').data('clear'),
            headers: {'X-CSRFToken': csrftoken},
            type: 'POST',
            data: {receipt_pk: receipt_pk},
            success: function (json) {
                console.log(json)
            }
        });
    };

    function credit(receipt_pk) {
        $.ajax({
            url: $('#receipts-list').data('credit'),
            headers: {'X-CSRFToken': csrftoken},
            type: 'POST',
            data: {receipt_pk: receipt_pk},
            success: function (json) {
                console.log(json)
            }
        });
    };

    $("#receipts-list").on('click', 'a[id^=clear-item-]', function (e) {
        e.preventDefault();
        var receipt_pk = $(this).attr('id').split('-')[2];
        console.log(receipt_pk);
        clear(receipt_pk)
    });
    $("#receipts-list").on('click', 'a[id^=credit-item-]', function (e) {
        e.preventDefault();
        var receipt_pk = $(this).attr('id').split('-')[2];
        console.log(receipt_pk);
        credit(receipt_pk)
    });
});
