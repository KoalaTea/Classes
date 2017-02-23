#!/usr/bin/php

<?php
    session_start();
    include("templates/template.php");
?>
<?php

$_SESSION["username"] = $username;


    try {
        // open connection to MongoDB server
        $conn = new Mongo('localhost');

        // access database
        $db = $conn->ChambordPi;

        // access collection
        $collection = $db->Users;


        $userName = $_POST['username'];
        $userPass = $_POST['password'];


        $user = $db->$collection->findOne(array('username'=> userName));

        if(is_null($user)){
            echo 'username incorrect';
        }else{
            foreach ($user as $obj) {
                echo 'Username' . $obj['username'];
                echo 'password: ' . $obj['password'];
                if($userName == 'user1' && crypt($userPass, $obj['password']) == $obj['password']){
                    echo 'found';            
                }
                else{
                    echo 'not found';            
                }

            }
        }
        // disconnect from server
        $conn->close();

    } catch (MongoConnectionException $e) {
        die('Error connecting to MongoDB server');
    } catch (MongoException $e) {
        die('Error: ' . $e->getMessage());
    }

$_SESSION["username"] = $correct;

?>

  <link rel="stylesheet" type="text/css" href="/static/css/login.css">

  <div class = "container">
    <div class="wrapper">
      <form action="" method="post" name="login" class="form-signin">
        <h3 class="form-signin-heading">Welcome... Please Authenticate</br>---------------</h3>
        <br>
        {{ form.hidden_tag() }}
        <input type="text" class="form-control" name="username" placeholder="Username" required="" />
        <input type="password" class="form-control" name="password" placeholder="Password" required=""/>

        <button class="btn btn-lg btn-red btn-block"  name="Submit" value="Sign In" type="submit"><b>/bin/bash</b></button>
      </form>
    </div>
  </div>

<?php include("templates/templatebottom.php") ?>
