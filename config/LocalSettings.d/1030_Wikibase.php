<?php
# 30_WikibaseSettings.php

# Load Wikibase extensions and configuration
$wgEnableWikibaseRepo = true;
#$wgEnableWikibaseClient = true;
wfLoadExtension('WikibaseRepository', "$IP/extensions/Wikibase/extension-repo.json");
require_once "$IP/extensions/Wikibase/repo/ExampleSettings.php";
#wfLoadExtension('WikibaseClient', "$IP/extensions/Wikibase/extension-client.json");
#require_once "$IP/extensions/Wikibase/client/ExampleSettings.php";
## WikibaseManifest Configuration
$wgWBRepoSettings['sparqlEndpoint'] = 'http://query.' . getenv('W4R_SERVER_NAME') . '/sparql';
$wgWBRepoSettings['string-limits']['VT:monolingualtext']['length'] = 100000;
# Wikibase Client
#wfLoadExtension('WikibaseLocalMedia');
#wfLoadExtension('WikibaseEdtf');
#wfLoadExtension('WikibaseManifest');
#wfLoadExtension('Babel');
#wfLoadExtension('EntitySchema');
