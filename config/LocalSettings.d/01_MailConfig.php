<?php

if (getenv('MAIL_HOST')) {
    # set smtp
    $wgSMTP = [
        'host' => getenv('MAIL_HOST'),
        'port' => getenv('MAIL_PORT'),
    ];
}

$wgPasswordSender = 'wiki@' . getenv('W4R_SERVER_NAME');
$wgEmergencyContact = getenv('W4R_MW_EMERGENCY_CONTACT');
