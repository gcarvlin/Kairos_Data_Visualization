<?php
if (isset($_POST['dylosNames']) && isset($_POST['bins']) && isset($_POST['t_from']) && isset($_POST['t_to'])) {
    $dNames = sanitizeString($_POST['dylosNames']);
    $bins = sanitizeString($_POST['bins']);
    $t_from = sanitizeString($_POST['t_from']);
    $t_to = sanitizeString($_POST['t_to']);
    echo passthru("python KC.py $dNames $bins $t_from $t_to");
}

function sanitizeString($var) {
    $var = stripslashes($var);
    $var = strip_tags($var);
    $var = htmlentities($var);
    return $var;
}


?>