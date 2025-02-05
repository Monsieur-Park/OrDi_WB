<?php
# 20_SemanticMediaWikiSettings.php

# Load Semantic MediaWiki extension
wfLoadExtension('SemanticMediaWiki');
enableSemantics(getenv('W4R_SERVER_NAME'));

$smwgQMaxInlineLimit = 10000;
$smwgQueryResultCacheType = CACHE_ANYTHING;
$smwgQueryResultCacheLifetime = 60 * 60 * 24 * 7;
