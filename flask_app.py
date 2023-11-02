"""server/app.py

Instantiated version of the Flask API.
"""
from terracotta import get_settings, logs
from terracotta.server import create_app
from flask_cors import CORS
import subprocess

settings = get_settings()

logs.set_logger(settings.LOGLEVEL, catch_warnings=True)

app = create_app(debug=settings.DEBUG, profile=settings.FLASK_PROFILE)


CORS(app, resources={
    r"/optimize-command": {"origins": "http://137.135.165.161"},
    r"/ingest-command": {"origins": "http://137.135.165.161"}
})

@app.route("/optimize-command")
def optimize_command():
    command_optimize = f"terracotta optimize-rasters /home/anup/b3d/code/b3d-backend/rasters/*.tif -o /home/anup/services/terracotta/optimized-rasters/  --skip-existing --compression lzw "
    subprocess.call(command_optimize, shell=True)
    return "<p>Success</p>"

@app.route("/ingest-command")
def ingest_command():
    command_ingest = "terracotta ingest /home/anup/services/terracotta/optimized-rasters/{name}_{band}.tif -o  /home/anup/services/terracotta/terracotta.sqlite --skip-existing"
    subprocess.call(command_ingest, shell=True)
    return "<p>Success</p>"
