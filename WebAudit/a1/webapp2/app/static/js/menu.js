function selectDrink(drinkname) {
  window.location = "review_order/"+drinkname;
}

function customDrink() {
  window.location = "custom_drink";
}

function cancelDrink(orderid) {
  $.post({
    url: "/cancel_drink",
    data: {
      order: orderid,
    }
  });
  location.reload(false);
}
