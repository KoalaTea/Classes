#!/usr/bin/php

<?php
	header('Content-type: text/html');
?>

<html>
    <head> 
        <title>Print the working directory.</title>
    <body bgcolor="white"> 
        <?php $browser = getenv('HTTP_USER_AGENT'); echo "The users browser is $browser\n"; 
        $vars = get_defined_vars(); echo "The vars are $vars\n";
        echo '<pre>'; print_r($vars); echo '</pre>'; ?>
    </body> 
</html>
