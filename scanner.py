import os
from pathlib import Path

def find_steam_root() -> Path:
    """
    return the first steam root path that exists on this machine
    raises a runtimeError if none are found
    """
    candidates = [
        Path("~/.local/share/Steam").expanduser(),
        Path("~/.steam/steam").expanduser()
    ]

    # TODO: loop through candidates and return the first that is a directory
    # Use: path.is_dir()

    print("Checking Steam root candidates...")
    for c in candidates:
        if c.is_dir():
            return c


    raise RuntimeError("Steam root not found")

def get_appmanifests(steamapps_path: Path) -> list[Path]:
    """
    this function grabs path of all steamapps from appmanifest
    and puts them in a sorted list
    """
    file_iterator = steamapps_path.glob("appmanifest_*.acf")
    file_list = list(file_iterator)
    file_list = sorted(file_list)
    return file_list

def read_text(path) -> str:
    """
    This function opens the manifest file and returns full text
    """
    return path.read_text(encoding="utf-8", errors="ignore")

def extract_quoted_value(text, key) -> str | None:
    """
    This function splits appmanifest text, uses [3] index to grab value of key
    """

    ### TODO add context of how appmanifest appears once get_appmanifest and read_text
    ### runs so that way this isnt just a bunch of trash code with no insight lol
    splitText = text.splitlines()

    for t in splitText:
        s = t.strip()
        if s.startswith(f'"{key}"'):
            value1 = s.split('"')
            value2 = value1[3]
            if len(value1) >= 4:
                return value2
            else: pass

    return None

def parse_manifest(manifest_path) -> tuple[str, str]:
    """
    This function is a full open of manifest, grab (appid, name) and return values one all
    """
    text = read_text(manifest_path)

    parsed_appid = extract_quoted_value(text, "appid")
    parsed_name = extract_quoted_value(text, "name")

    parsed_info = parsed_appid, parsed_name

    if any(item is None for item in parsed_info):
        raise RuntimeError(f"Parse failed for {manifest_path}!")

    return parsed_info

def unwanted_app_detect(name: str) -> bool:
    """
    This function checks for app names that are not actual games, like redists and compat tools
    then marks them with boolean value for later classification
    """
    unwanted_apps = ["proton",
                     "steam linux runtime",
                     "redistributables",
                     "eas anti-cheat runtime",
                     "easyanticheat runtime",
                     "steamworks common redistributables",
                     "vulkan shader",
                     "compatibility tool"]
    lowercase = name.lower()
    for i in unwanted_apps:
        if i in lowercase:
            return True

    return False

def classify_app(appid: str, name: str) -> str:
    """
    This function classifies app based on boolean value
    if marked as True, app is not a game
    if marked as False, app is a game
    """
    if unwanted_app_detect(name) == True:
        return "unwant"
    else: return "game"

def offline_risk(name: str) -> tuple[int, list[str]]:
    """
    This function takes name arg (game title string) and outputs
    (score, reasons) where score is 0-100
    0 is safest offline, 100 is most likely online only
    reasons is list of short explanations why score is what it is
    """
    score = 10
    reasoning = []

    # list of canidates whos name triggers score to be upped to 70
    strong_online_likely = [
        "overwatch",
        "destiny",
        "warzone",
        "apex",
        "fortnite",
        "valorant",
        "the finals",
        "dead by daylight",
        "hitman world of assassination",
        "steep"
        ]
    
    # list of canidates whos name has an online play keyword
    online_keywords = [
        "online",
        "multiplayer",
        "pvp",
        "mmo",
        "season",
        "battle pass",
        "live service"
    ]
    
    # list of some launcher keywords for name check
    ### TODO: Rockstar games are on my steam deck yet need to come up 
    ### with way for list of rockstar games inside this list as RDR2,
    ### GTAIV, and max payne 2 all considered "likely offline" with score of 10
    ### instead of intended score of 25. this list as of now is great 
    ### heuristically/relatively accurate but non functioning and stupid.
    launcher_keywords = [
        "rockstar",
        "ubisoft",
        "ea",
        "origin",
        "uplay",
        "2k",
        "bethesda"
    ]
    
    n = name.lower()
    for i in strong_online_likely:
        if i in n:
            score += 70
            reasoning.append("live service game and/or always online")
    for i in online_keywords:
        if i in n:
            score += 50
            reasoning.append("game most definitely has online mode, may be playable offline, though unlikely")
    for i in launcher_keywords:
        if i in n:
            score += 25
            reasoning.append("launcher detected, still chance of offline play")

    if score > 100: score = 100
    elif score < 0: score = 0

    return (score, reasoning)

def offline_label(score: int) -> str:
    """
    This function labels game's score with a str to determine offline playability
    """
    if score <= 25: return "Likely Offline"
    elif score > 25 and score <= 60: return "Risky Offline"
    elif score > 60: return "Unlikely Offline"


def main() -> None:
    steam_root = find_steam_root()
    # FOR DEBUG print(f"Steam root: {steam_root}")

    steamapps = steam_root / "steamapps"

    steam_appmanifest = get_appmanifests(steamapps)
    numOf_steam_appmanifest = len(steam_appmanifest)

    print(f"Found {numOf_steam_appmanifest} appmanifests.")

    games = []
    unwant = []

    for path in steam_appmanifest:
        appid, name = parse_manifest(path)
        if unwanted_app_detect(name):
            print(f"NOISE: {name}")
        else: print(f"GAME DETECTED: {name}")

    
        if classify_app(appid, name) == "unwant":
            unwant.append((appid, name))
        else: games.append((appid, name))

    print(f"This is the amount of games: {len(games)}")
    print(f"This is the amount of unwanted apps: {len(unwant)}")

    for appid, name in games:
        score, reasons = offline_risk(name)
        label = offline_label(score)
        print(f"{label} | {score} | {name}")
        if len(reasons) != 0: print(f"\n    {reasons}")



if __name__ == "__main__":
    main()