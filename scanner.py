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

    print("DEBUG CHECK: checking Steam root candidates...")
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


def main() -> None:
    steam_root = find_steam_root()
    print(f"Steam root: {steam_root}")

    steamapps = steam_root / "steamapps"
    library_vdf = steamapps / "libraryfolders.vdf"

    print(f"Steamapps: {steamapps}")
    print(f"Library file: {library_vdf}")
    print(f"Exists (answer as boolean): {library_vdf.is_file()}")

    steam_appmanifest = get_appmanifests(steamapps)
    numOf_steam_appmanifest = len(steam_appmanifest)
    print(f"Found {numOf_steam_appmanifest} appmanifests.")
    print("These are the first 5 of them: ")
    for path in steam_appmanifest[:5]:
        print(f"{path}")
    debug_input = input("Proceed with showing the first manifest? [y/n]: ")
    if debug_input == "y":
        first_manifest = steam_appmanifest[0]
        text = read_text(first_manifest)
        print("\n".join(text.splitlines()[:10]))
        debug_input = input("Proceed with extraction of values from manifest? [y/n]: ")
        if debug_input == "y":
            print(extract_quoted_value(text, "appid"))
            print(extract_quoted_value(text, "name"))
        else: pass
    else: pass

if __name__ == "__main__":
    main()