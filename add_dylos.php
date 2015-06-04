<?php //setupusers.php
  require_once 'login.php';
  $connection = new mysqli($hn, $un, $pw, $db);

  if ($connection->connect_error) die($connection->connect_error);

  $dylos = 'Dylos20,Dylos21,Dylos22,Dylos23,Dylos24,Dylos25';
  $username = 'Admin';

  add_dylos($connection, $dylos, $username);
  
  function add_dylos($connection, $dylos, $un)
  {
    $query  = "UPDATE users2 SET dylos='$dylos'
                WHERE username='$un'";
    $result = $connection->query($query);
    if (!$result) die($connection->error);
  }
?>
