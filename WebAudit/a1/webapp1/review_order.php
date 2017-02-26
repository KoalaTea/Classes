#!/usr/bin/php-cgi

#TODO FINISH

<?php include("templates/template.php"); ?>

<?php
    if(!(!is_null($_SESSION['username']) && $_SESSION['username'] != '')){
?>
    <script type="text/javascript">
     <!--
     window.location = "index.php"
     -->
     </script>
     You are not logged in, you cannot order a drink
<?php
     }else{
?>
    <link rel="stylesheet" type="text/css" href="/static/css/menu.css">
    <script type="text/javascript" src="/static/js/review_order.js"></script>

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
                      <b class="dir">~/menu/</b>]$ curl order | less
                    </h5>
                  </div>
              </div>
          </div>
          <div class="panel-body">
              <div class="tr">
                  <div class="td">
                    <div class="col col-xs-4" align=left>
                      <img height="100%" width="100%" src="{{url_for('static', filename='images/drinks/')}}{{img}}">
                    </div>
                    <div class="col col-xs-8" align=left>
<?php
               $drinkname = $_GET['drinkname'];
               $conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");
               $filter = [ 'name' => $drinkname ];
               $query = new MongoDB\Driver\Query($filter);
               $drinks = $conn->executeQuery('ChambordPi.Drinks', $query);

                        echo '<h3 class="drink-title"><b>' . $drinkname . '</b></h3>';
?>
                      <ul>
<?php
                   foreach( $drinks as $drink ){
                       foreach( $drink->recipe as $ingredient ){
                           echo '<li class="drink-text">' . $ingredient->amount;
                              if(!is_null($ingredient->flavor)){
                                echo ' ' . $ingredient->flavor;
                              }
                              echo ' ' . $ingredient->type;
?>
                          </li>
<?php                  
                      }
                }
?>
                      </ul>
                    </div>
                  </div>
              </div>
              <div class = "tr">
                <div class="col col-xs-12">
                  <div class="form-group">
                    <label class="drink-title" for="ordernotes">Enter any special requests:</label>
                    <textarea placeholder="Show me the moose..." class="form-control" id="instructOrder" rows="3"></textarea>
                  </div>
                  <div class="col col-xs-6">
                    <button style="width: 100%" id="cancelBtn" onclick="cancelOrder()" class="btn btn-primary btn-hover-green">Cancel</button>
                  </div>
                  <div class="col col-xs-6">
                    <button style="width: 100%" id="orderBtn" onclick="orderDrink('{{drinkname}}')" class="btn btn-danger">Order</button>
                  </div>
                </div>
              </div>
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
<?php } //end login check if?>
<?php include("templates/templatbottom.php"); ?>
