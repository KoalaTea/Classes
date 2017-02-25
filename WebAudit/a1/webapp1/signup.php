#!/usr/bin/php-cgi

<?php
// open connection to MongoDB server
$conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");

// access database
//$db = $conn->ChambordPi;

// access collection
//$collection = $db->Users;
function generateHash($password) {
    if (defined("CRYPT_BLOWFISH") && CRYPT_BLOWFISH) {
        $salt = '$2y$11$' . substr(md5(uniqid(rand(), true)), 0, 22);
        return crypt($password, $salt);
    }
}

echo generateHash('temporary2017koalatea');

$bulk = new MongoDB\Driver\BulkWrite;
$user1 = [ 'username' => 'koalatea2', 'password'=>generateHash('temporary2017koalatea'), 'credits'=> 100000, 'roles'=>Array( 'user', 'admin', 'bartender'), 'drinksOrdered' => 0 ];
$user2 = [ 'username' => 'user', 'password'=>generateHash('user'), 'credits'=> 1000, 'roles'=>Array( 'user' ), 'drinksOrdered' => 0 ];

$bulk->insert($user1);
$bulk->insert($user2);

$result = $conn->executeBulkWrite('ChambordPi.Users', $bulk);

echo "TEST!";
?>
