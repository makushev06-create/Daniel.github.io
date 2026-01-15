<?php 
require_once("db.php");

// Получаем данные из формы
$username = $_POST['username'];
$password = $_POST['password'];


if(empty($username) || empty($password))
{
    echo "Заполните все поля";
}
else {
    $sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    $result = $conn->query($sql);
}

if ($result->num_rows>0)
{
    while($row = $result->fetch_assoc()){
         header("Location: glav.html");
            exit(); // Завершаем выполнение скрипта
    }
   
}
 else {
        echo "Нет такого пользователля";
    }











?>