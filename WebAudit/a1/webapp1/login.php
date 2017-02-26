#!/usr/bin/php-cgi

<?php
    include("templates/template.php");
?>
<?php
    //function login(){
    echo var_dump($_SESSION);
    if((!is_null($_SESSION['username']) && $_SESSION['username'] != '')){
?>
    <script type="text/javascript">
    <!--
    //indow.location = "index.php"
    -->
    </script>
    You're already logged in, redirecting you.
<?php
    }else{
        if(isset($_GET['Submit'])){
            try {
                // open connection to MongoDB server
                $conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");
                
                // access database
                //$db = $conn->ChambordPi;

                // access collection
                //$collection = $db->Users;

                $userName = $_GET['username'];
                $userPass = $_GET['password'];

                $filter = [ "username" => $userName ];
                $query = new MongoDB\Driver\Query($filter);
                $user = $conn->executeQuery('ChambordPi.Users', $query);

                //$user = $collection->findOne(array('username'=> userName));
                if(is_null($user)){
                    echo 'username incorrect';
                }else{
                    foreach ($user as $obj) {
                        if($userName == $obj->username && crypt($userPass, $obj->password) == $obj->password){
                            $_SESSION['username'] = $userName;
                            $_SESSION['roles'] = $obj->roles;
                            var_dump($_SESSION['roles']);
                        }
                        else{
                            $_SESSION['username'] = '';
                        }

                    }
                }
                // disconnect from server
                //$conn->close();

            } catch (MongoConnectionException $e) {
                die('Error connecting to MongoDB server');
            } catch (MongoException $e) {
                die('Error: ' . $e->getMessage());
            }
        }
    }
//}
?>

  <link rel="stylesheet" type="text/css" href="/static/css/login.css">

  <div class = "container">
    <div class="wrapper">
      <form action="" method="get" name="/cgi-bin/login.php" class="form-signin">
        <h3 class="form-signin-heading">Welcome... Please Authenticate</br>---------------</h3>
        <br>
        <input type="text" class="form-control" name="username" placeholder="Username" required="" />
        <input type="password" class="form-control" name="password" placeholder="Password" required=""/>

        <button class="btn btn-lg btn-red btn-block"  name="Submit" value="Sign In" type="submit"><b>/bin/bash</b></button>
      </form>
    </div>
  </div>

<?php include("templates/templatebottom.php") ?>
