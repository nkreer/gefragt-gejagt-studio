<?php

// Script to export all the played questions

$data = json_decode(file_get_contents("export.json"), true);

$q = [];

foreach($data["questions"] as $question){
	if($question["played"]){
		$changed = $question;
		unset($changed["id"]);
		unset($changed["played"]);
		unset($changed["answerPlayer"]);
		unset($changed["answerChaser"]);
		$q[] = $changed;
	}
}
echo "Exported ".count($q)." questions\n";

file_put_contents("questionDump.json", json_encode($q, JSON_PRETTY_PRINT));