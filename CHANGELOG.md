# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html) while it uses a changelog format that is compatible with [chag](https://github.com/mtdowling/chag).

## Unreleased

### Changed

* Fixed starting torrents to work with rtorrent 0.9.7 by adapting the new api endpoint `load.raw_start` in favor of the deprecated `load_raw_start` endpoint
* Migrated codebase to work with python3

## 1.1.5 - 2017-07-26

### Fixed

* Fixed the exception handling to no longer cause TypeErrors; this behavior was introduced with 1.1.4.
  Now when an exception happens the application prints a FAIL and in the following lines the exception
  message and the traceback.

## 1.1.4 - 2017-07-24

### Fixed

* Fixed exception handling to not throw exceptions

## 1.1.3 - 2017-07-22

### Changed

* Updated changelog format

## 1.1.2 - 2017-07-22

### Added

* Added a link from README to CHANGELOG

### Changed

* Changed the tag naming scheme to have the prefix `v`

### Fixed

* Fixed 1.1.1 Improvements to be h2 instead of h1

## 1.1.1 - 2017-07-22

### Added

* Added an example to the README

## 1.1 - 2017-07-21

### Added

* Added exception handling in the case that the network or one of the hosts is down

### Changed

* Refactored the loading of the torrent content into a separate function

## 1.0 - 2017-07-16

### Added

* Implemented --verbose command line argument to reduce noise when running from a cronjob
* Added a great load of documentation to the README.md file

## 0.9 - 2017-07-16

### Added

* Implemented basic functionality to fetch RSS feeds, download the linked torrent file and invoke load_raw_start() on the XMLRPC interface of rtorrent

