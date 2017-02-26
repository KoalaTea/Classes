#!/usr/bin/php-cgi

<?php include("templates/template.php"); ?>

    <link rel="stylesheet" type="text/css" href="/static/css/orders.css">
    <script type="text/javascript" src="/static/js/menu.js"></script>

<?php
//TODO noworky
if((!is_null($_SESSION['username']) && $_SESSION['username'] != '' && (in_array('bartender', $_SESSION['roles']) || in_array('admin', $_SESSION['roles'])))){
?>
<div class="container" style="margin-top:5px">
  <div class="row">
    <div class="col">
      <div class="panel panel-default panel-table">
          <div class="panel-heading">
              <div class="tr">
                  <div class="td">
                    <h5 class="drink-title">
<?php
        echo '[<b class="user-name">' . $_SESSION['username'] . '</b>@<b class="hacker-bar">Hackerbar';
?>
                      </b>
                      <b class="dir">~/menu/</b>]$ cat orders | less
                    </h5>
                  </div>
              </div>
          </div>
          <div class="panel-body">
<?php
               $conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");
               $filter = [];
               $query = new MongoDB\Driver\Query($filter);
               $orders = $conn->executeQuery('ChambordPi.Orders', $query);

               //check if collection is empty
               if($orders->toArray()){
                   $orders = $conn->executeQuery('ChambordPi.Orders', $query);
                   foreach ( $orders as $order ){
                       echo "FICL";

?>
              {% if orders.length != 0 %}
              {% for order in orders %}
              <div class="tr">
                  <div class="td">
                    <div class="col col-xs-12" align=center>
                        {% if order['status']|lower == "queued" %}
                        <div class="col col-xs-4" align=left>
                          <h5 class="drink-title"><b>{{order['name']}}</b></h5>
                          <ul>
                            {% for ingredient in order['recipe'] %}
                              <li class="drink-text">{{ingredient['amount']}}
                                  {% if ingredient['flavor']|lower != "none" %}
                                    {{ingredient['flavor']}}
                                  {% endif %}
                                  {{ingredient['type']}}
                              </li>
                            {% endfor %}
                          </ul>
                          <form action="update_order" method="post" name="update_order" class="form-drinkupdate">
                            <input type="hidden" name="id" value= {{ order['_id'] }}>
                            <input type="hidden" name="status" value= {{ order['status'] }}>
<?php
                            if(strtolower($order->status)=="queued"){
                                echo '<button id="stepBtn" class="btn btn-primary btn-hover-green" type="submit">Mixing</button>';
                            }elseif(strtolower($order->status)=="inprogress"){
                                echo '<button id="stepBtn" class="btn btn-success btn-hover-green" type="submit">Ready</button>';
                            }elseif(strtolower($order->status)=="ready"){
                                echo '<button id="stepBtn" class="btn btn-danger btn-hover-green" type="submit">Picked Up</button>';
                            }
?>
                        </form>
                        </div>
                        <div class="col col-xs-8">
                          <div class="row">
                          </div>
                          <br>
                          <p>Notes: </p>
                          <label class="drink-text">{{order['instructions']}}</label>
                        </div>
                    </div>
                  </div>
              </div>
<?php         } //end orders for?>
<?php     }else{ ?>
              <h1> No Orders... </h1>
<?php     } //end if not empty?>    
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
<?php }else{ ?>
    <script type="text/javascript">
     <!--
     window.location = "index.php"
     -->
     </script>
     Must be a bartender.
<?php } ?>
<?php include("templates/templatebottom.php"); ?>
