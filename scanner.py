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

def main() -> None:
    steam_root = find_steam_root()
    print(f"Steam root: {steam_root}")

    steamapps = steam_root / "steamapps"
    library_vdf = steamapps / "libraryfolders.vdf"

    print(f"Steamapps: {steamapps}")
    print(f"Library file: {library_vdf}")
    print(f"Exists (answer as boolean): {library_vdf.is_file()}")


if __name__ == "__main__":
    main()