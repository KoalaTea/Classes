                    <h5 class="drink-title">

<?php
                    echo '[<b class="user-name">' . $_SESSION['username'] . '</b>@<b class="hacker-bar">Hackerbar'
?>
                      </b>
<?php
                        $conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");
                        $userfilter = [ 'username' => $_SESSION['username'] ];
                        $userquery =  new MongoDB\Driver\Query($userfilter);
                        $users = $conn->executeQuery('ChambordPi.Users', $userquery);
                        $userarray = $users->toArray();
                        $user = $userarray[0];

                        echo '<b class="dir">~/credits</b>]$ ' . $user->credits;
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
<?php
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
                  echo '<button id="orderBtn" onclick="selectDrink(\'' . $drink->name . '\')" class="btn btn-primary btn-hover-green">Place Order</button>';
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
