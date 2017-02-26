function selectDrink(drinkname) {
  window.location = "review_order.php/?drinkname="+drinkname;
}

function customDrink() {
  window.location = "custom_drink.php";
}

function cancelDrink(orderid) {
  $.get({
    url: "/cancel_drink.php",
    data: {
      order: orderid,
    }
  });
  location.reload(false);
}
