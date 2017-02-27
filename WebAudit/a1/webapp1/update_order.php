#!/usr/bin/php-cgi

<?php
                header('Content-type: text/html');
                session_start();
                if((!is_null($_SESSION['username']) && $_SESSION['username'] != '' && (in_array('bartender', $_SESSION['roles']) || in_array('admin', $_SESSION['roles'])))){
                    //our db
                    $id = $_GET['id'];
                    $status= $_GET['status'];
                    $conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");

                    //make our objid
                    $objid = new MongoDB\BSON\ObjectId($id);

                    //Get the order
                    $filter = [ '_id' => $objid ];
                    $query = new MongoDB\Driver\Query($filter);
                    $orders = $conn->executeQuery('ChambordPi.Orders', $query);
                    $orderarray = $orders->toArray();

                    //Get the user

                    //if drink exists
                    if($orderarray){
                        //set drink
                        $order = $orderarray[0];
                        //update the user
                        $bulk = new MongoDB\Driver\BulkWrite;
                        if($status == 'queued'){
                            $bulk->update(['_id'=>$objid], ['$set'=>['status'=>'inprogress']]);
                        }elseif($status == 'inprogress'){
                            $bulk->update(['_id'=>$objid], ['$set'=>['status'=>'ready']]);
                        }elseif($status == 'ready'){
                            //record the completed order
                            unset($order->_id);
                            $order->status='completed';
                            $bulk->insert($order);
                            $conn->executeBulkWrite('ChambordPi.PastOrders', $bulk);

                            //Get the user
                            $userfilter = [ 'username' => $order->user ];
                            $userquery =  new MongoDB\Driver\Query($userfilter);
                            $users = $conn->executeQuery('ChambordPi.Users', $userquery);
                            $userarray = $users->toArray();
                            $user = $userarray[0];

                            //change the users ordered drinks
                            $bulk = new MongoDB\Driver\BulkWrite;
                            $bulk->update(['username'=>$user->username], ['$set'=>['drinksOrdered'=>($user->drinksOrdered - 1)]]);
                            $conn->executeBulkWrite('ChambordPi.Users', $bulk);

                            //delete the order
                            $bulk = new MongoDB\Driver\BulkWrite;
                            $bulk->delete(['_id'=>$objid]);
                        }
                        $conn->executeBulkWrite('ChambordPi.Orders', $bulk);

?>
                      <script type="text/javascript">
                      <!--
                      window.location = "bartender.php"
                      -->
                      </script>
                      Action completed.
<?php
                    }else{
?>
                      <script type="text/javascript">
                      <!--
                      window.location = "bartender.php"
                      -->
                      </script>
                      Action failed.
<?php
                   }
                }else{
                    echo '{"status": "failed - not logged in, or not a bartender"}';
                }
?>
