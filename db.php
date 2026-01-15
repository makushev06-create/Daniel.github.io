<?php 


$servername = "localhost";
$username = "root";
$password = "";
$dbname = "learing";

$conn = mysqli_connect($servername, $username, $password, $dbname);

if(!$conn){
    die("Connection fialed" . mysqli_connect_errno());
}
else {
    echo "Успех";
}



?>






