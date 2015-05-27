<?php
$var1 = "Dylos20";
if (isset($_POST['dylosNames']) && isset($_POST['bins']) && isset($_POST['t_from']) && isset($_POST['t_to'])) {
    $dNames = $_POST['dylosNames'];
    $bins = $_POST['bins'];
    $t_from = $_POST['t_from'];
    $t_to = $_POST['t_to'];
    echo passthru("python KC.py $dNames $bins $t_from $t_to");
}
?>