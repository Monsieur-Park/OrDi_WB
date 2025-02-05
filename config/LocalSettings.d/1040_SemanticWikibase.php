<?php
# 30_WikibaseSettings.php


# Semantic Wikibase configuration
wfLoadExtension('SemanticWikibase');
$wgExtraNamespaces[WB_NS_PROPERTY] = 'WikibaseProperty';
$wgExtraNamespaces[WB_NS_PROPERTY_TALK] = 'WikibaseProperty_talk';

$wgHooks['CanonicalNamespaces'][] = static function (&$list) {
    global $wgExtraNamespaces;
    $wgExtraNamespaces[WB_NS_PROPERTY] = $list[WB_NS_PROPERTY] = 'Wikibase_property';
    $wgExtraNamespaces[WB_NS_PROPERTY_TALK] = $list[WB_NS_PROPERTY_TALK] = 'Wikibase_property_talk';
};

$wgGroupPermissions['user']['item-create'] = true;
$wgGroupPermissions['user']['property-create'] = true;
$wgSemanticWikibaseLanguage = 'de';
$smwgNamespacesWithSemanticLinks[WB_NS_PROPERTY] = true;
$smwgNamespacesWithSemanticLinks[WB_NS_ITEM] = true;



