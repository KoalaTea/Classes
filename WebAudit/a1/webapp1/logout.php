#!/usr/bin/php-cgi

<?php
    include("templates/template.php");
    if(!(!is_null($_SESSION['username']) && $_SESSION['username'] != '')){
?>
    <script type="text/javascript">
    <!--
    //window.location = "index.php"
    -->
    </script>
    You're not logged in, redirecting you.
<?php
    }else{
        session_destroy();
    }
//}
?>
    <script type="text/javascript">
    <!--
    window.location = "index.php"
    -->
    </script>
    You are now logged out, redirecting you.

  <link rel="stylesheet" type="text/css" href="/static/css/login.css">

<?php include("templates/templatebottom.php") ?>
