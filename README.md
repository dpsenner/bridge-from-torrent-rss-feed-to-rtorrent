# Introduction

This is a small tool that takes torrents from a rss feed and starts them on rtorrent.

# Usage

This section explains how to use the tool. Typically this tool can be run by simply running ./main.py with the right command line arguments.

The following example will fetch the RSS feeds from `http://rss-feed.host/rss-feed` and start all torrents on the rtorrent instance behind the uri `http://rtorrent.host/RPC2`.

```
~/bridge-from-torrent-rss-feed-to-rtorrent$ main.py \
--rss-feed-uri=http://rss-feed.host/rss-feed \
--xml-rpc-uri=http://rtorrent.host/RPC2
```

The following section explains all available command line arguments.

## Command line arguments

The tool accepts the following command line arguments:

### --xml-rpc-uri

This argument sets the uri to the rtorrent http xmlrpc interface. This argument is required.

#### Allowed values

Any uri string is allowed.

#### Default value

This argument is required but has no default value.

#### Example usage

```
--xml-rpc-uri=http://host-of-rtorrent/RPC2
```

### --rss-feed-uri

This argument sets the uri to the RSS feed. This argument is required.

#### Allowed values

Any uri string is allowed.

#### Default value

This argument is required but has no default value.

#### Example usage

```
--rss-feed-uri=http://host-of-rss-feed/path-to-rss-feed
```

### --rss-feed-cookie-key

This argument sets a cookie key to be used when retrieving the RSS feed and when fetching the torrent that a RSS feed link points to. This argument needs to be combined with a --rss-feed-cookie-value argument. The tool then interprets this argument as the cookie key and the next --rss-feed-cookie-value argument as the value of the cookie. The cookie key must argument must come before the cookie value argument.

#### Allowed values

Any string is allowed.

#### Default value

This argument is optional and has no default value.

#### Example usage

This example sets the cookie foo=bar when sending requests to fetch the RSS feed or fetch the torrent file referenced by a RSS feed link.

```
--rss-feed-cookie-key=foo --rss-feed-cookie-value=bar
```

### --rss-feed-cookie-value

This argument sets a cookie value to be used when retrieving the RSS feed and when fetching the torrent that a RSS feed link points to. This argument needs to be combined with a --rss-feed-cookie-key argument. The tool interprets this argument as the value of the cookie and the previous -rss-feed-cooki-key argument as the key of the cookie. The cookie value argument must come after the cookie key argument.

#### Allowed values

Any string is allowed.

#### Default value

This argument is optional and has no default value.

#### Example usage

This example sets the cookie foo=bar when sending requests to fetch the RSS feed or fetch the torrent file referenced by a RSS feed link.

```
--rss-feed-cookie-key=foo --rss-feed-cookie-value=bar
```

### --verbose

By default the tool runs verbosely (--verbose=yes), meaning that it outputs informational messages. When setting up the script to run as a cronjob it is wise to set --verbose=no to avoid causing crond to send emails when all is fine. It is better when crond only sends an email when it encounters a problem and it requires the attention of a human.

#### Allowed values

- yes
- no

#### Default value

- yes

#### Example usage

This example disables verbose outputs.

```
--verbose=no
```

# Installation

A typical installation would add the script as a cronjob that runs regularily every few minutes. This has the effect that new torrents in the rss feed are so started and downloaded. It further allows the script to send failures through the crond daemon. Please note that the script should not generate output when running as a cronjob so long all is fine.

## Requirements

These are the requirements for this tool to work:

- python2.7
- python-feedparser
- python-requests

### Install requirements on Ubuntu 16.04 LTS

This section explains how to install the requirements on ubuntu 16.04 LTS.

```
~$ sudo apt install python2.7 python-feedparser python-requests
```

### rtorrent requirements

Further rtorrent has to be installed with xmlrpc enabled. This can be achieved by configuring the .rtorrent.rc configuration file to contain the following.

```
# enable scgi support
scgi_port = 127.0.0.1:5000
```

### apache2 requirements

Further the scgi port enabled in rtorrent needs to be mounted in a apache2 site. This can be achieved by configuring a site (i.e. /etc/apache2.sites-enabled/default) to contain the SCGIMount directive.

Note that it is wise to not make the xml rpc interface accessible to anyone. Anyone would then be allowed to remotely control your rtorrent instance! Therefore this example further adds basic password protection to provide a minimum of security. Adding simple authentication makes it easy to provide the username and password in the xml rpc uri.

```
<VirtualHost *:80>
	...
	SCGIMount /RPC2 127.0.0.1:5000
	<Location /RPC2>
		AuthName "Auth required"
		AuthType Basic
		AuthBasicProvider file
		AuthUserFile /path-to/.htpasswd
		Require user allowed_user
	</Location>
	...
</VirtualHost>
```

Assuming that the "allowed_user" has the password "verysecurepassword" and runs on the host "rtorrent.host", the XML rpc uri argument would look like the following.

```
--xml-rpc-uri=http://allowed_user:verysecurepassword@rtorrent.host/RPC2
```

#### Remark: Transdroid

Having configured rtorrent and apache2 like this, we now also have set up our rtorrent instance to be controlled remotely with Transdroid from an Android device.

https://www.transdroid.org/

## Installation as a cronjob

- Make sure you have installed all the requirements
- Clone repository; this should automatically checkout the master branch which tracks the latest stable changeset
- Run the script to test if the arguments are fine
```
~/bridge-from-torrent-rss-feed-to-rtorrent/$ main.py --rss-feed-uri=http://rss-feed.host/rss-feed --xml-rpc-uri=http://rtorrent.host/RPC2
```
- Add cronjob by running as the user under which the cronjob should run by typing:
```
~/$ crontab -e
```
- Add the following lines at the end to run the script every 5 minutes:
```
*/5 * * * * /home/$user/bridge-from-torrent-rss-feed-to-rtorrent/main.py --xml-rpc-uri=http://rtorrent.host/RPC2 --rss-feed-uri=http://rss-feed.host/rss-feed --verbose=no
```
- Save the changes and exit the editor
- Done

Please note that it may be wise to write a simple intermediary script that is run by the cronjob and makes the crontab -e easier. A typical sample script could be:

```
#!/bin/bash
xml_rpc_uri="http://rtorrent.host/RPC2"
rss_feed_uri="http://rss-feed.host/rss-feed"

# REMARK: when running as a cronjob it needs to be an absolute path to the script
# set the $USER variable to the actual user that this command is run with if the
# $USER environment variable is not available
#USER=nobody

# run the command
/home/$USER/bridge-from-torrent-rss-feed-to-rtorrent/main.py \
--xml-rpc-uri="$xml_rpc_uri" \
--rss-feed-uri="$rss_feed_uri" \
--verbose=no

```

# Changelog

You can review the changelog of all past releases [here](CHANGELOG.md).

# Contributing

Please read the contributing guidelines before starting to work on a patch, writing issues or file a pull request. The contributing guidelines are available [here](CONTRIBUTING.md).

