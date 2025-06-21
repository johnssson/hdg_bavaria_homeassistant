## [0.7.3](https://github.com/banter240/hdg_bavaria_homeassistant/compare/v0.7.2...v0.7.3) (2025-06-21)

### 🐛 Bug Fixes

* fix(hdg_boiler): Reduce excessive INFO logging for unexpected API fields

The HDG boiler API frequently returns 'hidden' and 'background' fields which, while technically
"unexpected" based on the initial explicit field list, are consistently present and do not
indicate a functional issue. The current logging configuration results in a high volume of
INFO level messages for each data refresh, even in debug mode, leading to unnecessary log
spam and obscuring potentially more critical information.

This commit updates the `_async_handle_data_refresh_response` method in `api.py` to
explicitly include 'hidden' and 'background' in the set of expected fields. This change
ensures that the INFO log message "Item has unexpected fields" is only triggered for
truly new or unknown fields returned by the API, significantly reducing log output
without losing valuable information about genuinely unexpected data structures.

The core functionality of processing the API response remains unchanged, as these fields
were already being safely ignored. This is purely a logging refinement to improve system
observability and reduce noise.

## [0.7.2](https://github.com/banter240/hdg_bavaria_homeassistant/compare/v0.7.1...v0.7.2) (2025-06-21)

### 🐛 Bug Fixes

- fix(build): Correct ZIP archive structure for HACS

The previous version of the publish.sh script created a ZIP file containing a parent directory (e.g., hdg_boiler/).

This incorrect structure prevents HACS from correctly installing and loading the integration, as it expects the component's files (manifest.json, etc.) to be at the root of the archive.

This commit modifies the script to change directory into the component's source folder before running the zip command. By zipping the contents ('.') from within that directory, the resulting archive now has the correct flat structure required by HACS.

## [0.7.1](https://github.com/banter240/hdg_bavaria_homeassistant/compare/v0.7.0...v0.7.1) (2025-06-21)

### 🐛 Bug Fixes

- fix(release): Improve release notes format and clean up changelog

## [0.7.0](https://github.com/banter240/hdg_bavaria_homeassistant/compare/v0.6.1...v0.7.0) (2025-06-21)

### ✨ New Features

- **core:** Introduce background worker, dynamic polling, and full CI/CD pipeline ([70259d2](https://github.com/banter240/hdg_bavaria_homeassistant/commit/70259d204f5d5ddf741a4b2a9d1cc992f54005e1))

### 🐛 Bug Fixes

- **ci:** Prevent release workflow loop ([affb6a0](https://github.com/banter240/hdg_bavaria_homeassistant/commit/affb6a0f99e95483512fb7449d4a81b594e930af))
