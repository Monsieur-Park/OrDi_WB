<?php
# 00_BasicConfiguration.php

error_reporting(E_ALL & ~E_DEPRECATED);

# Protect against web entry
if (!defined('MEDIAWIKI')) {
    exit;
}

# Basic site information
$wgSitename = getenv('W4R_MW_WIKI_NAME');
$wgServer = getenv('W4R_FULL_SERVER_NAME');

# JobRunner instance is assumed by default, so jobs on request is disabled
$wgJobRunRate = 0;

# File Uploads enabled by default
$wgEnableUploads = true;

$wgScriptPath = "/w"; 
$wgArticlePath = "/wiki/$1";
$wgLoadScript = "/load.php";
$wgResourceBasePath = $wgScriptPath;

# Logo settings
$wgLogos = ['1x' => "images/logo.png"];
$wgFavicon = "/images/favicon.ico";


# Security keys
$wgSecretKey = "f7f20f9b6d90bc37df9b06adef361b599e6927700362b6f1cadccb3e6e94d917";
$wgUpgradeKey = "b61de951108ac967";

# Database settings
$wgDBserver = getenv('W4R_DB_SERVER');
$wgDBname = getenv('W4R_DB_NAME');
$wgDBuser = getenv('W4R_DB_USER');
$wgDBpassword = getenv('W4R_DB_PASS');
$wgDBprefix = "";
$wgDBTableOptions = "ENGINE=InnoDB, DEFAULT CHARSET=binary";

# Shared memory settings
$wgMainCacheType = CACHE_ACCEL;
$wgMemCachedServers = [];

#language settings
$wgLanguageCode = "en";
#$wgLanguageCode = "de-formal";