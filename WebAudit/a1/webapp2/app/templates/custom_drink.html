{% extends "base.html" %}

{% block head %}
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/menu.css') }}">
    <script type="text/javascript" src="/static/js/menu.js"></script>
    <script type="text/javascript" src="/static/js/custom_drink.js"></script>
{% endblock %}

{% block content %}
<div class="row">
  <div class="col col-xs-12">
    <div class="row">
    <select class="custom-select btn btn-primary mb-2 mr-sm-2 mb-sm-0" style="margin-left: 30px"id="amountSelector">
      <option value="1">1 oz</option>
      <option value="2">25%</option>
      <option value="3">50%</option>
      <option value="4">75%</option>
    </select>
    <select class="custom-select btn btn-primary mb-2 mr-sm-2 mb-sm-0" id="ingredientSelector">
      {% for ingredient in ingredients %}
      <option value="{{loop.index}}">
        {% if ingredient['flavor']|lower != "none" %}
          {{ingredient['flavor']}}
        {% endif %}
        {{ingredient['name']|capitalize}}
        {{ingredient['type']|capitalize}}
      </option>
      {% endfor %}
  </select>
  </div>
  <div class="row" align=right>
    <button style="margin-bottom: 5px; margin-right: 20px; margin-top: 5px; width: 100%" id="orderBtn" onclick="addIngredient()" class="btn btn-success">Add ingredient</button>
  </div>
  <h4 class="drink-title">Ingredients:</h4>
  <ul id="ingredientList">
  </ul>
</div>
<div class="col col-xs-12" style="position: fixed; bottom: 0;">
  <div class="form-group">
    <label class="drink-title" for="ordernotes">Enter any special requests:</label>
    <textarea placeholder="Show me the moose..." class="form-control" id="instructOrder" rows="3"></textarea>
  </div>
  <button style="width: 100%" id="submitBtn" onclick="orderCustom()" class="btn btn-primary">Place Order</button>
</div>
</div>
{% endblock %}
