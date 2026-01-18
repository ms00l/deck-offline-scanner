# Deck Offline Scanner

A local, offline-first analysis tool that scans a Steam installation and estimates **offline playability risk** for installed games.

Built specifically with **Steam Deck and Linux users** in mind, this tool analyzes Steam app manifests directly and applies heuristic scoring to determine how likely each game is to work without an internet connection.

---

## What This Tool Does

Deck Offline Scanner:

- Scans your local Steam installation
- Reads `appmanifest_*.acf` files
- Extracts:
  - App ID
  - Game name
- Filters out non-games such as:
  - Proton runtimes
  - Steam Linux runtimes
  - Redistributables
- Assigns each game an **offline risk score (0–100)**
- Labels each game as:
  - **Likely Offline**
  - **Risky Offline**
  - **Unlikely Offline**
- Explains *why* each score was assigned

All analysis is done **locally**, with no API calls or internet dependency.

---

## Why This Exists

Many Steam Deck users want to know:

- Which games will work on a plane
- What can be played without Wi-Fi
- Whether a launcher or live service dependency will block offline play

Existing resources (forums, ProtonDB, PCGamingWiki) are helpful, but they are:
- Not personalized
- Not offline
- Not integrated with your installed library

This tool fills that gap by providing a **local, explainable, heuristic-based assessment** of offline playability.

---

## How It Works (Conceptually)

The program is structured as a pipeline:

### 1. Steam Filesystem Scan

- Locates the Steam root directory
- Finds all `appmanifest_*.acf` files
- Reads manifest text directly

### 2. Manifest Parsing

Each manifest is parsed to extract:
- `appid`
- `name`

This creates structured `(appid, name)` records for each installed item.

### 3. Game vs Noise Classification

Before scoring, the program filters out:
- Proton versions
- Steam Linux runtimes
- Redistributables
- Compatibility tools

This ensures only actual games are evaluated.

### 4. Offline Risk Scoring

Each game name is evaluated using heuristics:
- Live-service keywords
- Online-only indicators
- Known launcher dependencies
- Multiplayer-focused naming patterns

Each factor increments a risk score and records a reason.

Scores are capped between `0–100`.

### 5. Human-Readable Labeling

Risk scores are mapped to labels:
- **Likely Offline**
- **Risky Offline**
- **Unlikely Offline**

Results are printed with both the score and reasoning.

---

## Example Output

```
Likely Offline | 10 | Max Payne 2: The Fall of Max Payne

Risky Offline | 35 | Red Dead Redemption 2
['launcher detected, still chance of offline play']

Unlikely Offline | 80 | HITMAN World of Assassination
['live service game and/or always online']
```


---

## Design Philosophy

- Offline-first
- No external APIs
- Heuristic, not hardcoded
- Explainable results
- Modular functions
- Easily extensible

The goal is not perfect accuracy, but **useful, defensible estimates** that improve over time.

---

## Current Limitations

- Risk scoring is heuristic-based and name-driven
- Some games may be misclassified due to naming ambiguity
- Launcher detection is simplistic
- No persistence or caching yet
- CLI output only

These limitations are intentional at this stage to keep the core logic clear and testable.

---

## Planned Improvements

Future development ideas include:

### Heuristic Refinement

- Better detection of single-player vs multiplayer
- More granular launcher handling
- Reduced false positives for known offline-capable games

### Data Enrichment

- Cached ProtonDB data
- PCGamingWiki flags
- Offline play indicators stored locally

### Output Enhancements

- JSON or CSV export
- Sorting and filtering
- Saved scan results

### GUI

- Simple table view
- Sort by offline risk
- Filter by label
- Click to view reasoning per game

The current architecture supports all of these without major refactoring.

---

## Who This Is For

- Steam Deck users
- Linux gamers
- Travelers
- Offline-first players
- Anyone curious about their library’s offline reliability

---