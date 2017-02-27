#!/usr/bin/php-cgi

<?php include("templates/template.php"); ?>
<?php
     if(!(!is_null($_SESSION['username']) && $_SESSION['username'] != '')){
?>
      <script type="text/javascript">
      <!--
      window.location = "index.php"
      -->
      </script>
      You are not logged in, you do not have reccent drinks
<?php 
     }else{
                     $conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");

                     $userfilter = [ 'username' => $_SESSION['username'] ];
                     $userquery =  new MongoDB\Driver\Query($userfilter);
                     $users = $conn->executeQuery('ChambordPi.Users', $userquery);
                     $userarray = $users->toArray();

                     $user = $userarray[0];

                $filter = [ 'user' => $_SESSION['username'] ];
                $query = new MongoDB\Driver\Query($filter);
                $orders = $conn->executeQuery('ChambordPi.Orders', $query);
                $ordersArray = $orders->toArray();

?>

    <link rel="stylesheet" type="text/css" href="/static/css/orders.css">
    <script type="text/javascript" src="/static/js/menu.js"></script>

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
<?php
                     echo '<b class="dir">~/credits</b>]$ ' . $user->credits;
?>
                    </h5><h5 class="drink-title">
<?php
                     echo '[<b class="user-name">' . $_SESSION['username'] . '</b>@<b class="hacker-bar">Hackerbar';
?>
                      </b>
<?php
                      echo '<b class="dir">~/total_drinks</b>]$ ' . $user->drinksOrdered;
?>
                    </h5>
                    <h5 class="drink-title">
<?php
                      echo '[<b class="user-name">' . $_SESSION['username'] . '</b>@<b class="hacker-bar">Hackerbar';
?>
                      </b>
                      <b class="dir">~/status/</b>]$ cat orders | less
                    </h5>
                  </div>
              </div>
          </div>
          <div class="panel-body">
<?php
              if($ordersArray){
                foreach($ordersArray as $order){
                    if(strtolower($order->status) != "complete"){
?>
              <div class="tr">
                  <div class="td">
                    <div class="col col-xs-12" align=right>
                      <div class="col col-xs-4" align=center>
<?php
                        echo '<h3 class="drink-title"><b>' . $order->name .'</b></h3>';
                        echo '<img height="100%" width="100%" src="/static/images/drinks/' . $order->image . '">';
?>
                        <div class="row">
                          <div class="col">
                            <div class="panel panel-default panel-table">
                             <div class="tr">
<?php
                        echo '<button width="100%" style="margin-bottom: 5px" id="orderAgainBtn" onclick="selectDrink(\'' . $order->name . '\')" class="btn btn-primary btn-hover-green">Order Again</button>'
?>
                             </div>
<?php
                            if(strtolower($order->status) == "queued"){
?>
                              <div class="tr">
<?php
                                echo '<button width="100%" id="cancelBtn" onclick="cancelDrink(\'' . $order->_id . '\')" class="btn btn-danger">Cancel Order</button>';
?>
                              </div>
<?php } //ends if queued ?>
                           </div>
                          </div>
                        </div>
                      </div>
                      <div class="col col-xs-8">
                        <div class="row">
                        <h4 class="order-status"> Status:</h4>
<?php
                        if(strtolower($order->status) == "queued"){
?>    
                        <h4 class="order-queued">Queued</h4>
                        <progress value="25" max="100"></progress>
<?php
                       }elseif(strtolower($order->status) == "inprogress"){
?>
                        <h4 class="order-inprogress">Mixing Now</h4>
                        <progress value="75" max="100"></progress>
<?php
                       }elseif(strtolower($order->status) == "ready"){
?>
                        <h4 class="order-ready">Ready</h4>
                        <progress value="100" max="100"></progress>
<?php } //end the elseifs above ?>
                        </div>
                        <br>
                        <div class="col">
<?php
                           echo '<label class="drink-text">' . $order->instructions . '</label>';
?>
                        </div>
                      </div>
                    </div>
                  </div>
              </div>
<?php
                    }//end completed if
                }//end orders loop
              }else{
?>
              <h1 class="drink-title"> No Orders... </h1>
<?php
            } //end if orders
?>
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

<?php } //end login check?>
<?php include("templates/templatebottom.php"); ?>
