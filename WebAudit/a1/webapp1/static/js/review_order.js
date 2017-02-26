function orderDrink(drinkname) {
  var inst = document.getElementById("instructOrder").value;
  $.get({
    url: "/order_drink.php",
    data: {
      drink: drinkname,
      instructions: inst
    }
  });
  window.location = "/recent_orders";
}
function cancelOrder(){
  window.location = "menu";
}
