            <h5 class="drink-title">
                      [<b class="user-name">Guest</b>@<b class="hacker-bar">Hackerbar
                      </b>
                      <b class="dir">~/menu/</b>]$ ls -l | less
		    </h5>
                  </div>
              </div>
          </div>
          <div class="panel-body">
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
