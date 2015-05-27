<?php // authenticate.php, modified from: http://lpmj.net/4thedition/  Example 12-4
  $hn = 'localhost';
  $db = 'auth';
  $un = 'root';
  $pw = '';
  $connection = new mysqli($hn, $un, $pw, $db);
  
  function redirect($url) {
    ob_start();
    header('Location: '.$url);
    ob_end_flush();
    die();
    }

  if ($connection->connect_error) die($connection->connect_error);

  if (isset($_SERVER['PHP_AUTH_USER']) &&
      isset($_SERVER['PHP_AUTH_PW']))
  {
    $un_temp = mysql_entities_fix_string($connection, $_SERVER['PHP_AUTH_USER']);
    $pw_temp = mysql_entities_fix_string($connection, $_SERVER['PHP_AUTH_PW']);

    $query  = "SELECT * FROM users2 WHERE username='$un_temp'";
    $result = $connection->query($query);
    if (!$result) die($connection->error);
    elseif ($result->num_rows)
    {
        $row = $result->fetch_array(MYSQLI_NUM);

		$result->close();

        $salt1 = "qm&h*";
        $salt2 = "pg!@";
        $token = hash('ripemd128', "$salt1$pw_temp$salt2");

        if ($token == $row[2]) {
            $query = "SELECT dylos FROM users2 WHERE username='$un_temp'";
            $result = $connection->query($query);
            if (!$result) die($connection->error);
            $row = $result->fetch_array(MYSQLI_NUM);
            $result->close();
            session_start();
            $_SESSION['dylos'] = $row[0];
            redirect("gviz.html");}
        else die("Invalid username/password combination");
    }
    else die("Invalid username/password combination");
  }
  else
  {
    header('WWW-Authenticate: Basic realm="Restricted Section"');
    header('HTTP/1.0 401 Unauthorized');
    die ("Please enter your username and password");
  }

  $connection->close();

  function mysql_entities_fix_string($connection, $string)
  {
    return htmlentities(mysql_fix_string($connection, $string));
  }	

  function mysql_fix_string($connection, $string)
  {
    if (get_magic_quotes_gpc()) $string = stripslashes($string);
    return $connection->real_escape_string($string);
  }
?>
