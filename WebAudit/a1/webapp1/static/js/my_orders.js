function get_orders(){
    $.ajax({
        url: '/my_current_orders',
        type: 'GET', // GET or POST
        success: function(data) { // data is the response from your php script
            $('#output').html(data);
        },
        error: function() {
            // This callback is called if your AJAX query has failed
            alert("Error!");
        }
    });
};
