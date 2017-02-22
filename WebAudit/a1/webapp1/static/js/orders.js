//$(document).ready(function()){
var isClosed = true;
var updating = window.setInterval(reload_orders, 5000);

function reload_orders(){
    $.ajax({
        url: '/current_orders',
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

function order_complete( orderid ){
    $.ajax({
        url: "/order_complete",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ _id : orderid }), 
        success: function(data) {
             $('#output').html(data);
       },
        error: function(data) {
            alert("ERROR");
        }
    });
};

function toggle_update(){
    if(!updating){
        updating = window.setInterval(reload_orders, 5000);
    }else{
        window.clearInterval(updating);
        updating = null;
    }
}

//if x closes the bar restart the update, if remove bottle, change the complete button to auto update
//the rest of the drinks (nah lets just make a global update button that will update the flow of
//drinks based off of the less alchohol
function slide_bar(id, alchoholtype, flavor) {
  if (isClosed == false) {     
    //overlay.hide();
    $("." + id + "." + alchoholtype + "." + flavor).removeClass('is-open');
    $("." + id + "." + alchoholtype + "." + flavor).addClass('is-closed');
    //document.getElementsByClassName(id + " " + alchoholtype + " " + flavor).removeClass('is-open');
    //document.getElementsByClassName(id + " " + alchoholtype + " " + flavor).addClass('is-closed');
    isClosed = true;
    toggle_update();
  } else {   
    //overlay.show();
    $("." + id + "." + alchoholtype + "." + flavor).removeClass('is-closed');
    $("." + id + "." + alchoholtype + "." + flavor).addClass('is-open');
    //document.getElementsByClassName(id + " " + alchoholtype + " " + flavor).removeClass('is-closed');
    //document.getElementsByClassName(id + " " + alchoholtype + " " + flavor).addClass('is-open');
    isClosed = false;
    toggle_update();
  }
}
  
//  $('[data-toggle="offcanvas"]').click(function () {
//        $('#wrapper').toggleClass('toggled');
//  });  
//});


