<link rel="stylesheet" type="text/css" href="/static/css/menu.css">
<script type="text/javascript" src="/static/js/menu.js"></script>

<div class="container" style="margin-top:5px">
  <div class="row">
    <div class="col">
      <div class="panel panel-default panel-table">
          <div class="panel-heading">
              <div class="tr">
                  <div class="td">
                    <h5 class="drink-title">
                      [<b class="user-name">Guest</b>@<b class="hacker-bar">Hackerbar
                      </b>
                      <b class="dir">~/menu/</b>]$ ls -l | less
		    </h5>
                  </div>
              </div>
          </div>
          <div class="panel-body">
              <div class="tr" id="CustomDrink">
                <div class="td">
                  <div class="col col-xs-4" align=left>
                    <img style="height: 100%; width: 100%;" src="{{url_for('static', filename='images/drinks/')}}custom_drink.png">
                  </div>
                  <div class="col col-xs-8" align=left>
                    <h3 class="drink-title"><b>Custom</b></h3>
                    <ul>
                        <li class="drink-text">Design a drink of your own!</li>
                    </ul>
                  </div>
                </div>
	      </div>
              {% for drink in drinks %}
              {% set drinkname = drink['name'] %}
              {% set img = drink['image'] %}
              <div class="tr">
                  <div class="td">
                    <div class="col col-xs-4" align=left>
                      <img height="100%" width="100%" src="{{url_for('static', filename='images/drinks/')}}{{img}}">
                    </div>
                    <div class="col col-xs-8" align=left>
                      <h3 class="drink-title"><b>{{drinkname}}</b></h3>
                      <h5 class="drink-text">Cost: {{drink['cost']}}</h5>
                      <ul>
                        {% for ingredient in drink['recipe'] %}
                          <li class="drink-text">{{ingredient['amount']}}
                              {% if ingredient['flavor']|lower != "none" %}
                                {{ingredient['flavor']}}
                              {% endif %}
                              {{ingredient['type']}}
                          </li>
                        {% endfor %}
                      </ul>
                    </div>
                  </div>
              </div>
              {% endfor %}
          </div>
