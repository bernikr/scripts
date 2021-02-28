import os
import re

DOWNLOAD_PATH = "X:/TV/.autodownload/"
LIBRARY_PATH = "X:/TV/"

VIDEO_EXT = ["mkv", "mp4"]
SUB_EXT = ["srt"]


def get_all_files_in_subfolders(root):
    for path, subdirs, files in os.walk(root):
        for name in files:
                yield os.path.join(path, name)


if __name__ == '__main__':
    for ep_name in os.listdir(DOWNLOAD_PATH):
        ep_path = os.path.join(DOWNLOAD_PATH, ep_name)
        name, se_shorthand, s, e, extra = re.match(r"(.*)\.([sS](\d+)(?:[eE](\d+))+)\.?(.*)", ep_name).groups()
        if os.path.isdir(ep_path):
            show_name = name.replace('.', ' ').title()
            if not os.path.isdir(os.path.join(LIBRARY_PATH, show_name)):
                print(f"show dir not found: {show_name}")
                continue
            season_dir = os.path.join(LIBRARY_PATH, show_name, f"Season {s}")
            if not os.path.isdir(season_dir):
                os.mkdir(season_dir)
            video = False
            for filepath in get_all_files_in_subfolders(ep_path):
                path, file = os.path.split(os.path.join(ep_path, filepath))
                ext = file.split('.')[-1].lower()
                if ext in VIDEO_EXT:
                    video = True
                    extra = re.match(r".+[sS]\d+(?:[eE]\d+)+.?(.*)", file).group(1)
                    filename = f"{show_name} {se_shorthand.upper()} - {extra}"
                    origin = os.path.join(path, file)
                    destination = os.path.join(season_dir, filename)
                    os.rename(origin, destination)
                    print(f"moved {show_name} {se_shorthand}")
                elif exit in SUB_EXT:
                    pass
            if not video:
                print(f"No video file found for {ep_path}")
                continue

        elif os.path.isfile(ep_path):
            print("Raw file episodes currently not supported")