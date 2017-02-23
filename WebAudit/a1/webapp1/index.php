#!/usr/bin/php

<?php include("templates/template.php") ?>
        <p> 
        <?php $browser = getenv('HTTP_USER_AGENT'); echo "The users browser is $browser\n"; 
        $vars = get_defined_vars(); echo "The vars are $vars\n";
        echo '<pre>'; print_r($vars); echo '</pre>'; ?>
	</p>
<?php include("templates/templatebottom.php") ?>
