function orderDrink(drinkname) {
  var inst = document.getElementById("instructOrder").value;
  $.get({
    url: "/cgi-bin/order_drink.php",
    data: {
      drink: drinkname,
      instructions: inst
    }
  });
  window.location = "/cgi-bin/recent_orders.php";
}
function cancelOrder(){
  window.location = "/cgi-bin/menu.php";
}
