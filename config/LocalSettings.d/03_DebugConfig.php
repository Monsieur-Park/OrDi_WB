<?php
# 10_DebugSettings.php

# Debug settings for development environment
if (getenv('ENVIRONMENT') == 'dev') {
    $wgShowExceptionDetails = true;
    $wgDebugToolbar = true;
    $wgMaxPPNodeCount = 10000000; # Needed for large template usages
    $wgDebugLogFile = "/var/www/html/cache/debug.log";
}
