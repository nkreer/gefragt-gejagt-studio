<?php

// Converts a question tsv file to a playable json file for the software

$questions = explode("\n", file_get_contents("questions.tsv"));

shuffle($questions);

$json = [];

foreach($questions as $questionId => $question){
	$question = explode("	", $question);

	// Basic information
	$output = [];
	$output["id"] = $questionId;
	$output["type"] = ($question[1] == "Jagdrunde" ? 2 : 1);
	$output["category"] = $question[9];
	$output["level"] = $question[10];

	switch($question[1]){
	case 'Jagdrunde':
		$output["text"] = $question[2];
		$output["correctAnswer"] = $question[3];
		$output["wrongAnswers"] = [$question[4], $question[5], $question[6]];

		break;
	default:
		$output["text"] = $question[7];
		$output["correctAnswer"] = $question[8];
		$output["wrongAnswers"] = [];
	}

	if(rand(1, 8) == 1){
		$json[] = $output;
	}
}

file_put_contents("questions.json", json_encode($json, JSON_PRETTY_PRINT));
echo "Export complete. (".count($json)." questions)\n";