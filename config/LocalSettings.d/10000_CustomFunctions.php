<?php
# 50_CustomFunctions.php

# Custom parser hook examples
$wgHooks['ParserFirstCallInit'][] = function (Parser $parser) {
    MediaWiki\MediaWikiServices::getInstance()->getContentLanguage()->mMagicExtensions['stringToColor'] = ['stringToColor', 'stringToColor'];
    $parser->setFunctionHook('stringToColor', 'stringToColor');
};

function stringToColor(Parser $parser, $inputstring)
{
    $colors = array(
        "LemonChiffon", "LightGoldenRodYellow", "PapayaWhip", "Moccasin",
        "PeachPuff", "PaleGoldenRod", "Khaki", "PaleTurquoise", "LightBlue",
        "LightSteelBlue", "LightSkyBlue", "PowderBlue", "SkyBlue", "AliceBlue",
        "Honeydew", "MintCream", "Azure", "Lavender", "Thistle", "Plum",
        "LavenderBlush", "MistyRose", "Pink", "LightPink", "PeachPuff",
        "LightCoral", "LightSalmon", "LightCyan", "PaleGreen", "LightGreen"
    );

    $inputInteger = crc32($inputstring);
    $colorIndex = $inputInteger % count($colors);
    $selectedColor = $colors[$colorIndex];

    return $selectedColor;
}
