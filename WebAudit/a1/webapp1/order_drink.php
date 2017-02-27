#!/usr/bin/php-cgi

<?php
                header('Content-type: text/html');
                session_start();
                if((!is_null($_SESSION['username']) && $_SESSION['username'] != '')){
                    //our db
                    $name = $_GET['drink'];
                    $conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");

                    //Get the drink
                    $filter = [ 'name' => $name ];
                    $query = new MongoDB\Driver\Query($filter);
                    $drinks = $conn->executeQuery('ChambordPi.Drinks', $query);
                    $drinkarray = $drinks->toArray();

                    //Get the user
                    $userfilter = [ 'username' => $_SESSION['username'] ];
                    $userquery =  new MongoDB\Driver\Query($userfilter);
                    $users = $conn->executeQuery('ChambordPi.Users', $userquery);
                    $userarray = $users->toArray();

                    $user = $userarray[0];
                    //if drink exists
                    if($drinkarray){
                        //set drink
                        $drink = $drinkarray[0];
                        //if the user can afford
                        if($drink->cost <= $user->credits){
                            //make the order
                            $bulk = new MongoDB\Driver\BulkWrite;
                            $order = [ 'name'=>$drink->name, 'cost'=>$drink->cost, 'type'=>$drink->cost, 'timeOrdered'=>'lol todo', 'user'=>$_SESSION['username'], 'recipe'=>$drink->recipe, 'instructions'=>$_GET['instructions'], 'status'=>'queued', 'image'=>$drink->image ];
                            $bulk->insert($order);
                            $conn->executeBulkWrite('ChambordPi.Orders', $bulk);

                            //update the user
                            $bulk = new MongoDB\Driver\BulkWrite;
                            $bulk->update(['username'=>$_SESSION['username']], ['$set'=>['credits'=>($user->credits - $drink->cost), 'drinksOrdered'=>($user->drinksOrdered + 1)]]);
                            $conn->executeBulkWrite('ChambordPi.Users', $bulk);
                        }
                        echo '{"status": "okay"}';
                    }else{
                        echo '{"status": "failed - no such drink"}';
                    }
                }else{
                    echo '{"status": "failed - not logged in"}';
                }
?>
