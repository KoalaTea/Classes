function orderDrink(drinkname) {
  var inst = document.getElementById("instructOrder").value;
  $.post({
    url: "/order_drink",
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
