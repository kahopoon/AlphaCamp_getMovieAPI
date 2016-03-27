<?php

$raw_result = json_decode(shell_exec('python ./movie.py'));
$result = array("results" => $raw_result);

header("Content-type: application/json; charset=utf-8");
print(json_encode($result, JSON_UNESCAPED_UNICODE));

?>
