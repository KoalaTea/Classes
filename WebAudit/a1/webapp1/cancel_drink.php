#!/usr/bin/php-cgi

<?php
                header('Content-type: text/html');
                session_start();
                if((!is_null($_SESSION['username']) && $_SESSION['username'] != '')){
                    //our db
                    $id = $_GET['order'];
                    $conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");
                    
                    $objid = new MongoDB\BSON\ObjectId($id);

                    //Get the order
                    $filter = [ '_id' => $objid ];
                    $query = new MongoDB\Driver\Query($filter);
                    $orders = $conn->executeQuery('ChambordPi.Orders', $query);
                    $orderarray = $orders->toArray();

                    //Get the user
                    $userfilter = [ 'username' => $_SESSION['username'] ];
                    $userquery =  new MongoDB\Driver\Query($userfilter);
                    $users = $conn->executeQuery('ChambordPi.Users', $userquery);
                    $userarray = $users->toArray();

                    $user = $userarray[0];
                    //if drink exists
                    if($orderarray){
                        //set drink
                        $order = $orderarray[0];
                        //update the user
                        $bulk = new MongoDB\Driver\BulkWrite;
                        $bulk->update(['username'=>$_SESSION['username']], ['$set'=>['credits'=>($user->credits + $order->cost), 'drinksOrdered'=>($user->drinksOrdered - 1)]]);
                        $conn->executeBulkWrite('ChambordPi.Users', $bulk);

                        //delete the drink
                        $bulk = new MongoDB\Driver\BulkWrite;
                        $bulk->delete(['_id'=> $objid ]);
                        $conn->executeBulkWrite('ChambordPi.Orders', $bulk);

                        echo '{"status": "okay"}';
                    }else{
                        echo '{"status": "failed - no such drink"}';
                    }
                }else{
                    echo '{"status": "failed - not logged in"}';
                }
?>
