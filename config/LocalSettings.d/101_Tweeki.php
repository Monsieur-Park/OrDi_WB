<?php


# Enabled skins
wfLoadSkin('Tweeki');

$wgDefaultUserOptions['tweeki-advanced'] = 1;
//$wgTweekiSkinNavigationalElements = array('edit' => 'selft::edit');
$wgTweekiSkinHideAnon = ['sidebar-right' => true];
$wgTweekiSkinGridNone = [
      "mainoffset" => 0,
      "mainwidth" => 12
];
