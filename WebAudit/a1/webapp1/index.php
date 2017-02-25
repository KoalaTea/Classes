#!/usr/bin/php-cgi

<?php include("templates/template.php") ?>
        <p> 
        <?php $browser = getenv('HTTP_USER_AGENT'); echo "The users browser is $browser\n"; 
        $vars = get_defined_vars(); echo "The vars are $vars\n";
        echo '<pre>'; print_r($vars); echo '</pre>'; 
        var_dump($_SESSION);?>
	</p>
<?php include("templates/templatebottom.php") ?>
