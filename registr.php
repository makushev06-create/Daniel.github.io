<?php
require_once("db.php");

$username=$_POST['username'];
    $password=$_POST['password'];
$repeatpass=$_POST['repeatpass'];
$email = $_POST['email'];


if(empty($username) || empty($password)  || empty($email)          ){


echo "Заполните все поля";




}
else {

if($password != $repeatpass){
    echo "Пароли не совпадают";
}else{

$sql="INSERT INTO users (username, password, email) VALUES ('$username', '$password', '$email')";
if ($conn -> query($sql) === TRUE){
 header("Location: glav.html");
            exit(); // Завершаем выполнение скрипта

}
else{
    echo "Ошибка: " . $conn->error;
}
}

}
















?>