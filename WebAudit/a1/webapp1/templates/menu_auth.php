<?php
    session_start();
                    echo '[<b class="user-name">' . $_SESSION['username'] . '</b>@<b class="hacker-bar">Hackerbar'
?>
                      </b>
<?php
                       echo '<b class="dir">~/credits</b>]$' //idk yet{{credits}}
?>
                    </h5>
                    <h5 class="drink-title">
<?php
                    echo '[<b class="user-name">' . $_SESSION['username'] . '</b>@<b class="hacker-bar">Hackerbar'
?>
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
                    <button style="width: 117%;" id="customBtn" onclick="customDrink()" class="btn btn-primary btn-hover-green">Design</button>
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
                      <button id="orderBtn" onclick="selectDrink('{{drinkname}}')" class="btn btn-primary btn-hover-green">Place Order</button>
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
          <div class="panel-footer">
              <div class="tr" align=center>
                  <div class="td">
                  <h5 class="drink-title">(END)</h5>
                  </div>
              </div>
          </div>
      </div>
    </div>
  </div>
</div>
