# Changelog

Every noteable change is logged here.

## v0.13.2

## v0.13.1

## v0.13.0

### Feature

* add method to load page marks from path (7b396fffd8ab)

### Fix

* solve linter warning (6444cf39c385)
* do not overwrite findings ids (dd56908a3f2e)

## v0.12.7

## v0.12.6

### Feature

* support RangedLocations (9db49687d05c)

### Fix

* fix spelling error (c7fbca5abdf4)
* disable justified alignment (e3d70e6789f8)
* fix image path name (eea522621163)

## v0.12.5

### Fix

* introduce threshold to avoid miss printing (78c6eb6ec1c0)

## v0.12.4

### Feature

* use different page sizes to display rotated (db69dcfcc169)
* add font rise to text renderer (acc1e7208b34)

## v0.12.3

## v0.12.2

### Fix

* fix style closing (8e4e1f4d47d4)
* do not fail on missing font flags (77bf7bbe3954)

## v0.12.1

### Feature

* load marks depending on given `linters` (2b594d047794)

### Fix

* ensure to avoid unnecessary digits (daeebc9a4ac9)

## v0.12.0

### Feature

* change test to check marked words (497bdeda3e37)
* add word selection processor to cli (b529cc1b718e)
* load sentence marks and combine with selected text (5e07a7a3df06)
* add method to convert sentence findings to single words (c06c6f8164ac)
* add sentence matcher to match words to sentence (871cc76a8c09)
* use new style merger (930f93677999)
* validate style order (ae1d0e9eeef4)
* use words algorithm to split token (4f358bfaf830)

### Fix

* load word position correctly (d9e1ef6abab5)
* merge overlapping sections correctly (fbd17f971662)

### Documentation

* fix spelling error (9ea0193b33e0)

## v0.11.4

### Feature

* select alignment depending on extracted (8db73eeadfb0)
* add alignment loader (f5d718fdaa9b)
* add justified text as default (82731910775c)

### Fix

* add missing bounding rendering (5cc2d2b6cfd1)

## v0.11.3

## v0.11.2

### Fix

* sort required test resources (1c0e05129509)
* reduce digits and white spaces in output (9d833a9fe17c)

## v0.11.1

### Feature

* add horizontals and lines as input resource to render (60fbc4f48496)

## v0.11.0

### Feature

* add first simple approach of a table renderer (e53664b14996)
* load lines in html view data (b4f03a683ac2)
* add text style renderer (e306c67f7e4f)
* include change of text rise, flag and font to text printer (f5924e5fdee0)
* use simple hr renderer instead of generic line renderer (e769501edd57)
* add horizontal line renderer (8b5a605d136c)
* render horizontal lines in feedback view (38b5fd3df273)
* add method to render lines (081876130063)

### Fix

* use correct layout template and render line more clear (5db43f51535b)
* solve linter warnings (54714467c2cd)

### Documentation

* extend interface documentation (f4da2a840369)
* extend interface documentation (8a3e577ce99a)

## v0.10.1

### Fix

* add support for multiple inputs -i (06d00ce021d4)

## v0.10.0

### Feature

* add step to copy extracted images to generated html view (a959568f4a00)
* add image renderer to feedback view (420080d24202)
* extend image loader (2157d53d6300)
* add image raw loader (8e732007602a)
* add image information loader (fbf61dbe3014)
* add render multiline text feature (0db4bb24fc55)

## v0.9.0

### Feature

* finalize and refactor new precise html view (df81f796c35a)
* change to general marker approach (b6c6ff08ba0a)
* add strategy to unite multiple styles (ee53fc4a6239)

### Documentation

* add purpose of given test (60356af383cd)

## v0.8.3

## v0.8.2

### Feature

* use rectangle renderer for failure 3030 and 3031 (e80f01fffa97)
* skip mouse interaction on printed elements (c20d36e6f0e8)
* add id to finding to show/hide it later (89c492ca8691)

### Fix

* renderer page content first to make content override able (b05d83b49288)
* shrink html output (d5b559158428)

### Documentation

* extend interface documentation (db7fd9e27258)

## v0.8.1

### Fix

* add missing boxes resource (49b052afc62e)

## v0.8.0

### Feature

* extends renderer to draw user boxes (0e3b8997dcd4)
* add boxes to display user defined rectangles (8083e441fc75)

## v0.7.5

## v0.7.4

### Fix

* make shapes visible and clickable (a734c55d69fc)

## v0.7.3

### Fix

* correct code replacement (cf6efaa99e92)

## v0.7.2

### Fix

* fix problem in utila handling `.tmp folder` (e67cede9e5ca)

## v0.7.1

## v0.7.0

### Feature

* add reference to access added content border (6b682303410a)
* add reference to refer renderer object directly (60de63322d63)
* change content border to dotted style (ca7173d5615c)
* add border shape renderer to console (347b75e8f4a5)
* extend shape renderer to render content-border (66b400990f06)
* use BoundingLocation to draw rectangles in view (61ff5a9cf53b)
* make problem view modifiable (462599e369e1)
* enable dynamic input parameter (5d3f5dc77c9c)
* add option to render shapes in the background of html page (49cbed7c2491)
* add shape renderer to render figures to html page (3a7a0512446e)

### Fix

* add import to help yaml loader (337303af9b01)
* support to collect from multiple sources (6cd9c454958e)
* solve cyclic import (f6b047cd0c5f)

### Documentation

* add module purpose of `view` (1b2fe19f8f92)

## v0.6.4

## v0.6.3

## v0.6.2

## v0.6.1

## v0.6.0

### Feature

* add mark selector to problem view generator (d057ee76cd1e)
* link and activate problems renderer (11b2518532a5)
* add method to load required data from path (a8318a4c4199)
* add step interface to run problem renderer (5f93fccf9543)
* add method to group Findings by type(word, oneline) (8d099f783b37)
* add id to access different pages (4bfc28e545f5)
* handle white space and white lines correctly (0915f3d6c476)
* use PageMarkConfiguration to mark highlights words and lines (3221132be15f)
* add LineMarker to mark lines in renderer (fbbc0f0a9029)
* add marker mechanism to html renderer (60e94b917f9c)
* add word marker to add unique id for select words. (8c489be347d7)
* add renderer to convert text data to html view (dbafac0fee15)

### Fix

* fix import location (3482599880fb)
* add missing import (28e21c76ebad)
* fix variable assignment logic (1c2220134e9e)

### Documentation

* Happy New Year! (93d2f24ae212)
* extend interface documentation (a12ce8b3ab13)
* extend interface documentation (671666501a64)

## v0.5.1

### Feature

* add new rst doc structure (5db430e14d3d)

## v0.5.0

### Feature

* add linter results to pages result view (30dc85d31266)
* add linter to prepare findings for preview (d4f6a2f9e4ea)
* add draft to represent linter view (51ad3cc229b6)

## v0.4.15

### Fix

* do not open generated page automatically (920d8ed49b4a)

## v0.4.14

## v0.4.13

## v0.4.12

### Fix

* add missing report template to setup/installation package (a96b55992433)

## v0.4.11

## v0.4.10

## v0.4.9

## v0.4.8

## v0.4.7

## v0.4.6

### Feature

* expose naming to use in `queuemo` (923ea04984ba)

## v0.4.5

## v0.4.4

### Fix

* fix output data path due `featurepack` (0be4981db350)

## v0.4.3

### Fix

* fix input path to `featurepack` pattern (62bafcdb891a)

## v0.4.2

### Fix

* fix data input to `featurepack` structure (b29cdb461fee)

## v0.4.1

## v0.4.0

### Feature

* add workplan to generate view due `feedback` tool (3b7ac8c4645f)
* add horizontal line and page numbers to view report (c0bf7b6f7b3d)
* add feature to generate view with pdf content - draft (8af945cdf624)
* add new tool `feedback` to generate main report view (c8ae1f90f290)

### Fix

* remove duplicated requirement (0bbb75fe3e07)

## v0.3.0

### Feature

* use new feature function from utila package (78f6263fd040)
* improve the clarity of a workplan (f3442a432c42)

### Fix

* fix spelling error in header (b90955d8bbab)

### Documentation

* add basic information to readme (fe59f3944af0)

## v0.2.9

## v0.2.8

### Feature

* add ugly font view generation (a5c7a003cb22)

### Fix

* add missing templates to copy job (4ed76d6a2074)
* rename test data to correct data pattern (1a5202f8557b)

## v0.2.7

### Feature

* add hit the box renderer (6b629219e7f5)
* add feature selector - remove later after utila upgrade (b434b6ee1b7e)

## v0.2.6

### Fix

* avoid out of container overflow (4890643abca5)

## v0.2.5

### Fix

* fix scrambled order of return parameter (dd6df3aee668)

## v0.2.4

## v0.2.3

### Fix

* if file exists, command line must fail (f973e81cc80c)
* rename file to new convention (1d14fa4ad71d)

## v0.2.2

### Feature

* pass data from folder (b2fbb0a946d1)

## v0.2.1

### Feature

* print error message when missing resources (f4d028c4913d)
* a description and shortcut for cmdline tool (f205a19cff99)

### Fix

* catch empty resources and produce help view (91958e378589)

## v0.2.0

### Feature

* print help if nothing is passed to cmdinterface (7cdb8adc7560)
* add command line interface to run generation of statistica result (2414e714059a)
* split result template in two parts (aa79d82879ce)

### Fix

* use the single parameter, not the tuple (4a6bbc909a03)
* add missing template to copy templates while installing (b0da2d743d05)

## v0.1.1

## v0.1.0

### Feature

* basic implementation of feedback script (75c6f7931d16)

### Fix

* fix syntax-errors from baw setup template (5d98a2e35507)

## v0.0.0 Initial release

