var ingred = [];
function addIngredient(cost) {
  var ul = document.getElementById("ingredientList");
  var li = document.createElement("li");
  var e1 = document.getElementById("amountSelector");
  var g1 = e1.options[e1.selectedIndex].text;
  var e2 = document.getElementById("ingredientSelector");
  var g2 = e2.options[e2.selectedIndex].text;
  li.appendChild(document.createTextNode(g1+" "+g2));
  li.className = "drink-text"
  ingred.push(g1+" "+g2)
  ul.appendChild(li);
}

function orderCustom() {
  var inst = document.getElementById("instructOrder").value;
  $.post({
    url: "/order_custom_drink",
    data: {
      recipe: ingred,
      instructions: inst
    }
  });
  window.location = "/recent_orders";
}
