# Selection API Discussion

- [1. Overview](#1-Overview)
  - [1.1. Design Principles](#11-design-principles)
  - [1.2. Feature Requirements](#12-feature-requirements)
  - [1.3. Example Use Cases](#13-example-use-cases)
- [2. ipyaladin interfaces](#2-ipyaladin-interfaces)
  - [2.1. GET](#21-get)
  - [2.2. SELECT](#22-select)
- [3. aladin-lite interfaces](#3-aladin-lite-interfaces)
  - [3.1. Listeners](#31-Listeners)
  - [3.2. GET](#32-get)
  - [3.3. SELECT](#33-select)
  - [3.4. Misc](#34-misc)

# 1. Overview

We are building tools for the Roman Research Nexus platform to enable
scientists to analyze data from the Nancy Grace Roman Space Telescope.
As part of this effort, we are developing a suite of interoperable tools
within a JupyterLab environment, including integration with Aladin Lite.

To support scientific workflows, we aim to expose Aladin Lite\'s
features programmatically. Our initial focus is on selection
functionality, which is foundational for many analysis use cases.

We evaluated the current selection features available in ipyaladin, and
prototyped programmatic extensions to support:

- selecting a list of sources
  [[PR](https://github.com/pcuste1/ipyaladin/pull/2)]

- selecting sources within a region
  [[PR](https://github.com/pcuste1/ipyaladin/pull/1)].

These proofs-of-concept worked by reaching into internal components of
Aladin Lite. However, a more robust and maintainable solution requires
official API support.

This document outlines:

- our design principles

- feature requirements

- API specifications for both Aladin Lite and ipyaladin

- several motivating use cases.

## 1.1. Design Principles

#### Standard Interface Pattern

For each feature exposed by **aladin-lite** that we intend to support,
the interface should consistently offer the following APIs:

- **Listener**: Allows developers to attach callbacks to respond to
  relevant events.

- **Get**: Retrieves the current state or value of the feature.

- **Set (Select)**: Updates the feature\'s state programmatically. 

- **Misc:** Features that support the other 3,

This pattern ensures clarity, predictability, and ease of use across all
supported functionality.

#### Separation of Concerns

It is essential to clearly distinguish between the roles of the
ipyaladin and aladin-lite APIs. While many capabilities in ipyaladin
serve as direct proxies for aladin-lite features, this is not always the
case. ipyaladin is a higher-level interface that may combine
multiple aladin-lite operations to deliver more integrated or complex
functionality.

For example, although aladin-lite may expose individual APIs for
selecting catalog objects and footprints, ipyaladin might provide a
unified API that coordinates both actions under a single interface call.

#### Consistent Data Formats

To streamline development and enhance user experience, all ipyaladin
interfaces are expected to rely on Astropy-defined object formats (e.g.,
[Table](https://docs.astropy.org/en/stable/table/index.html),
[Region](https://astropy-regions.readthedocs.io/en/stable/)).
This provides a familiar and well-documented foundation for users
working within the scientific Python ecosystem.

#### User-Defined Catalogs

All selection interfaces are designed with the assumption that catalogs
are loaded into aladin-lite programmatically by the user within their
Jupyter notebook. Catalogs added directly via the widget interface are
not considered within the scope of these APIs, ensuring greater control
and consistency for programmatic workflows.

## 1.2. Feature Requirements

#### Selection Requirements

As a notebook user/scientist I want to\...

- slect a source within a catalog using a programmatic API

- select a list of sources within all loaded catalogs using a
  programmatic API

- select all sources within a defined region using a programmatic API

- select a footprint using a programmatic API 

#### Data Retrieval Requirements 

As a notebook user/scientist I want to\...

- access the list of currently selected sources using a programmatic
  API 

- access the region of currently selected sources, if one was used to
  select the sources, using a programmatic API 

- access the footprint currently selected using a programmatic API 

#### Listener Requirements 

As a developer, I want to\...

- listen for changes to the selected sources 

- listen for changes to the selection region

- listen for changes to the selected footprint

#### Misc. Requirements

As a notebook user/scientist I want to\...

- be able to remove the current selection using a programmatic API

## 1.3. Example Use Cases

**Use case 1:** A scientist is interested in all sources in a catalog
with a redshift within a defined range. The query might look like the
following
```
aladin.selectSources(match_func: lambda source: source.rshift > 1 and
source.rshift < 2)
```
**Use case 2:** A scientist is interested in a subset of the sources in
a catalog. Since they loaded the catalog themselves, they know that
there is an objId  field that uniquely identifies the source. The query
might look like the following 
```
aladin.selectSources(sources=catalog_subset, match_key="objId")
```
maybe they instead want to use RA and DEC to identify the source instead
```
aladin.selectSources(sources=catalog_subset, match_keys=["ra",
"dec"])
```
**Use case 3:** A software engineer wants to create an interoperable
layer between an aladin-lite widget and another visualization tool, such
as [jdaviz](https://jdaviz.readthedocs.io/en/stable/). They would then
need to use a combination of the APIs listed in this doc to ensure that
selection in aladin-lite are reflected in jdaviz and vice versa. 

# 2. ipyaladin interfaces

## 2.1. GET

#### GetSelection
```
def GetSelection() -> Table
```
Returns an Astropy table containing the currently selected catalog
sources

#### GetRegion
```
def GetRegion() -> Region
```
Returns an Astropy Region with the currently selected region (if
applicable)

#### GetFootprint 
```
def GetFootprint() -> Footprint
```
This method returns the currently selected footprint

## 2.2. SELECT

#### SelectSources

A few alternatives are provided for the selection functionality. Each
has potential use cases and should be considered. 

##### Option 1:
```
def SelectSources(selection: Table, match_keys: List[Str]) -> None
```
Send a request to aladin-lite to select a list of catalog sources
defined in an astropy table with a list of keys to match on

  **Parameter**   |**Type**                                                       |**Description**
  --------------- |-------------------------------------------------------------- |-----------------------------------------------------
  selection       |[Table](https://docs.astropy.org/en/stable/table/index.html)   |Table of catalog sources to select
  match_keys      |List[Str]                                                      |Keys within the table to use to match a source in the selection table to the sources loaded in aladin-lite catalogs
  ------------------------------------------------------------------------------------------------------------------------------------

##### Option 2:
```
def SelectSources(selection: Table, match_key: Str) -> None
```
Send a request to aladin-lite to select a list of catalog sources
defined in an astropy table with a single key to match on

  **Parameter**   |**Type**                                                       |**Description**
  --------------- |-------------------------------------------------------------- |--------------------------------------------------------
  selection       |[Table](https://docs.astropy.org/en/stable/table/index.html)   |Table of catalog sources to select

  match_key       |Str                                                            |Key within the table to use to match a source in the selection table to the sources loaded in aladin-lite catalogs
  ---------------------------------------------------------------------------------------------------------------------------------------

##### Option 3:
```
def SelectSources(match_func: Callable) -> None
```
Sends a request to aladin-lite to select all catalog sources that match
the provided function 

  **Parameter**   |**Type**   |**Description**
  --------------- |---------- |-----------------------------------------------------
  match_func      |lambda     |Lambda expression that defines that matching criteria for sources
  --------------------------------------------------------------------------------

#### SelectRegion
```
def SelectRegion(region: Region) -> None
```
This method triggers a selection by region event based on the coordinates 

  **Parameter**   |**Type**                                                                                            |**Description**
  --------------- |---------------------------------------------------------------------------------------------------| -------------------------------------------------------
  region          |[Region](https://astropy-regions.readthedocs.io/en/stable/api/regions.Region.html#regions.Region)   |The region corresponding to the sky coordinates that the user would like to select sources within
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### SelectFootprint
```
def SelectFootprint(footprint: Footprint) -> None
```
This method triggers a selection event on a user provided footprint

  **Parameter**   |**Type**    |**Description**
  --------------- |----------- |---------------------------------------------
  footprint       |Footprint   |The footprint the user would like to select

  -------------------------------------------------------------------------

# 3. aladin-lite interfaces

## 3.1. Listeners

Supported listeners that enable us to attach callback functions to
events that occur within aladin-lite.

  **Event Name**     |**Description**              |**Data**            |**Supported**
  ------------------ |---------------------------- |------------------- |---------------
  objectsSelected    |Fired when objects are selected by region, represents the individual objects selected |List of sources     |Existing
  regionsSelected    |Fired when objects are selected by region, represents the region used to select the objects    |Shape of the region selected|New
  objectClicked      |Fires when an object is clicked | Catalog object and xy coordinates of the click event | Existing
  footprintClicked   |Fires when a footprint is clicked | Footprint object xy coordinates of the click event | Existing
  -----------------------------------------------------------------------------------

## 3.2. GET

#### GetSelectedSources
```
/**
 * @returns List[Sources]
 */
function GetSelectedSources()
```
Returns the list of currently selected source objects.

#### GetSelectedRegion
```
/**
 * @returns Region
 */
function GetSelectedRegion()
```
Returns the region definition of the selection event, if a region was
used to select. 

#### GetSelectedFootprints
```
/**
 *@returns List[Footprint]
 */
function GetSelectedFootprints()
```
Returns the currently selected footprints

## 3.3. SELECT

#### SelectSources 

##### Option 1: 
```
/**
 * @param sources: List[Source]
 * @param keys: List[str]
 */
function SelectSources(sources, keys)
```
Selects the list of sources provided within aladin-lite

  **Parameter**   |**Type**         |**Description**
  --------------- |---------------- |--------------------------------------------
  sources         |List[Source]     |The list of sources to select.
  keys            |List[str]        |The list of keys to use to determine a match
  -----------------------------------------------------------------------------

##### Option 2:
```
/**
 * @param match_func: func()
 */
function SelectSources(match_func)
```
Selects the list of sources provided. Uses the match_func provided to
determine if a source should be selected

  **Parameter**   |**Type**    |**Description**
  --------------- |----------- |---------------------------------------------------
  match_func      |func(a,b)   |The function used to determine if an object should be selected

  -------------------------------------------------------------------------------

#### SelectRegion
```
/**
 * @param region: Region
 */
function SelectRegion(region)
```
Triggers a region selection within aladin-lite widget

  **Parameter**             |**Type**          |**Description**
  ------------------------- |----------------- |---------------------------
  region                    |Region            |The region to select objects within

  -----------------------------------------------------------------------

#### SelectFootprint
```
/**
 * @param footprint: Footprint
 */
function SelectFootprint(footprint)
```
Triggers a footprint selection within aladin-lite widget

  **Parameter**       |**Type**         | **Description**
  ------------------- |---------------- |-----------------------------------
  footprint           |Footprint        |The footprint to select


## 3.4. Misc

#### RemoveSelection
```
function RemoveSelection(()
```
Removes the current selection from aladin-lite widget.
