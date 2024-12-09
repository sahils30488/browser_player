import os

from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
MAIN_FOLDER = "/home/sahil/Downloads/"  # Root folder containing subfolders and videos


def get_video_paths(root_folder):
    """Fetch all video file paths recursively and sort them."""
    video_paths = []
    for root, dirs, files in os.walk(root_folder):
        relative_path = os.path.relpath(root, root_folder)
        # Ensure folders and files are sorted
        dirs.sort()  # Sort directories to maintain order
        files.sort()  # Sort files alphabetically
        for file in files:
            if file.endswith((".mp4", ".webm", ".avi")):
                # Create the desired format: relative_path/filename
                video_path = os.path.join(relative_path, file).replace("\\", "/")
                video_paths.append(video_path)
    return video_paths


@app.route("/", methods=["GET", "POST"])
def index():
    """Renders the video player and handles folder change."""
    global MAIN_FOLDER

    if request.method == "POST":
        new_folder = request.form.get("folder_path")
        if new_folder and os.path.isdir(new_folder):  # Check if folder exists
            MAIN_FOLDER = new_folder

    videos = get_video_paths(MAIN_FOLDER)
    return render_template("index.html", videos=videos, current_folder=MAIN_FOLDER)


@app.route("/video/<path:filename>", methods=["GET"])
def get_video(filename):
    """Serves the requested video file."""
    return send_from_directory(MAIN_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)
