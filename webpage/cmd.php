<?php

$domain = $_POST["domain"];
$subdomain = $_POST["subdomain"];
$scantype = $_POST["scantype"];
$networkscan = $_POST["networkscan"];

$cmd = 'curl -X POST -d \'{"input": "{\"subdomain\": \"'.$subdomain.'\", \"domain\": \"'.$domain.'\", \"scantype\": \"'.$scantype.'\", \"networkscan\": \"'.$networkscan.'\"}","stateMachineArn": "arn:aws:states:us-east-1:933490194069:stateMachine:MyStateMachine"}\' https://tibixp4ej5.execute-api.us-east-1.amazonaws.com/alpha/execution';
//echo "<pre>$cmd</pre>";

$output = shell_exec($cmd);


if ($scantype == "lite" && $networkscan == "no") {
        sleep(150);                   
} elseif ($scantype == "intensive" && $networkscan == "no") {
        sleep(300); 
} else {
        sleep(210);
}
                                             
header('Location: http://52.90.86.38/vapt/output.html');

echo "<pre>$output</pre>";
?>
