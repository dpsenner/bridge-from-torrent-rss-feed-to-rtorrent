This is a small tool that takes torrents from a rss feed and starts them on rtorrent.

# Usage

This section explains how to use the tool.

## Command line arguments

The tool accepts the following command line arguments:

### --xml-rpc-uri

Sets the XML RPC Uri to the . This argument is required.

#### Allowed values

Any uri string is allowed.

#### Default value

This argument is required but has no default value.

#### Example usage

```
--xml-rpc-uri=http://host-of-rtorrent/RPC2
```

### --rss-feed-uri

Sets the RSS Feed Uri. This argument is required.

#### Allowed values

Any uri string is allowed.

#### Default value

This argument is required but has no default value.

#### Example usage

```
--rss-feed-uri=http://host-of-rss-feed/path-to-rss-feed
```

### --rss-feed-cookie-key

Sets a cookie to be used when retrieving the RSS feed and when fetching the torrent that a RSS feed link points to. The tool interprets each --rss-feed-cookie-key and --rss-feed-cookie-value argument in the order that they are given on the command line. The cookie key must argument must come before the cookie value argument.

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

Sets a cookie to be used when retrieving the RSS feed and when fetching the torrent that a RSS feed link points to. The tool interprets each --rss-feed-cookie-key and --rss-feed-cookie-value argument in the order that they are given on the command line. The cookie key must argument must come before the cookie value argument.

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

```
--verbose=yes
```

## Example

```
main.py --rss-feed-uri=http://rss-feed.host/rss-feed --xml-rpc-uri=http://rtorrent-host/RPC2
```

## Installation

A typical installation would add the script as a cronjob that runs regularily every few minutes. This has the effect that new torrents in the rss feed are so started and downloaded. It further allows the script to send failures through the crond daemon. Please note that the script should not generate output so long all is fine.

# Requirements

These are the requirements for this tool to work:

- python2.7
- python-feedparser
- python-requests

## Installation

This section explains how to install the requirements.

### Ubuntu 16.04 LTS

This section explains how to install the requirements on ubuntu 16.04 LTS.

```
apt install python2.7 python-feedparser python-requests
```
