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
    if unwanted_app_detect(name) == True:
        return "unwant"
    else: return "game"

def main() -> None:
    steam_root = find_steam_root()
    # print(f"Steam root: {steam_root}")

    steamapps = steam_root / "steamapps"

    """
    ####### this was for debug
    # library_vdf = steamapps / "libraryfolders.vdf"
    # print(f"Steamapps: {steamapps}")
    # print(f"Library file: {library_vdf}")
    # print(f"Exists (answer as boolean): {library_vdf.is_file()}")
    """
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


    """
    ####### this was for debug
    # debug_input = input("Proceed with showing the first manifest? [y/n]: ")
    # if debug_input == "y":
    #     text = read_text(first_manifest)
    #     print("\n".join(text.splitlines()[:10]))
    #     debug_input = input("Proceed with extraction of values from manifest? [y/n]: ")
    #     if debug_input == "y":
    #         print(extract_quoted_value(text, "appid"))
    #         print(extract_quoted_value(text, "name"))
    #     else: pass
    # elif debug_input == "n":
    #     print("Moving on to parsing the first manifest in full...")
    """

if __name__ == "__main__":
    main()