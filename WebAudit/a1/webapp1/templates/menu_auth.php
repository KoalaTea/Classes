                    <h5 class="drink-title">

<?php
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
                    <img style="height: 100%; width: 100%;" src="/static/images/drinks/custom_drink.png">
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
<?php
              $conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");
              $filter = [];
              $query = new MongoDB\Driver\Query($filter);
              $drinks = $conn->executeQuery('ChambordPi.Drinks', $query);

              foreach ( $drinks as $drink ){
?>
              <div class="tr">
                  <div class="td">
                    <div class="col col-xs-4" align=left>
<?php
                  echo '<img height="100%" width="100%" src="/static/images/drinks/' . $drink->image . '">';
                  echo '<button id="orderBtn" onclick="selectDrink(' . $drink->name . ')" class="btn btn-primary btn-hover-green">Place Order</button>';
?>
                    </div>
                    <div class="col col-xs-8" align=left>
<?php
                      echo '<h3 class="drink-title"><b>' . $drink->name . '</b></h3>';
                      echo '<h5 class="drink-text">Cost:' . $drink->cost . '</h5>';
?>
                      <ul>
<?php
                        foreach ($drink->recipe as $ingredient){
                            echo '<li class="drink-text">' . $ingredient->amount;
                            if(!is_null($ingredient->flavor)){
                                echo ' ' . $ingredient->flavor;
                            }
                            echo ' ' . $ingredient->type;
?>
                          </li>
<?php } ?>
                      </ul>
                    </div>
                  </div>
              </div>
<?php } ?>
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
