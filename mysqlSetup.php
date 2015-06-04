<?php //setupusers.php
  require_once 'login.php';
  $connection = new mysqli($hn, $un, $pw, $db);

  if ($connection->connect_error) die($connection->connect_error);
  
  /*$query = "CREATE DATABASE auth";
  $result = $connection->query($query);
  if (!$result) die($connection->error);*/

  $query = "CREATE TABLE users2 (
    dylos VARCHAR(800) NOT NULL,
    username VARCHAR(32) NOT NULL UNIQUE,
    password VARCHAR(32) NOT NULL
  )";
  //$result = $connection->query($query);
  //if (!$result) die($connection->error);

  $salt1    = "qm&h*";
  $salt2    = "pg!@";

  $dylos = 'Dylos25';
  $username = 'CCV';
  $password = 'password';
  $token    = hash('ripemd128', "$salt1$password$salt2");

  add_user($connection, $dylos, $username, $token);

  $dylos = 'Dylos20,Dylos21,Dylos22,Dylos23,Dylos24,Dylos25';
  $username = 'Admin';
  $password = 'password';
  $token    = hash('ripemd128', "$salt1$password$salt2");

  add_user($connection, $dylos, $username, $token);

  function add_user($connection, $fn, $un, $pw)
  {
    $query  = "INSERT INTO users2 VALUES('$fn', '$un', '$pw')";
    $result = $connection->query($query);
    if (!$result) die($connection->error);
  }
?>
