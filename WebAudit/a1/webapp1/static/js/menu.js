function selectDrink(drinkname) {
  window.location = "review_order.php?drinkname="+drinkname;
}

function customDrink() {
  window.location = "/cgi-bin/custom_drink.php";
}

function cancelDrink(orderid) {
  $.get({
    url: "/cgi-bin/cancel_drink.php",
    data: {
      order: orderid,
    }
  });
  location.reload(false);
}
