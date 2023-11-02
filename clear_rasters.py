import subprocess

delete_media = "sudo rm media/Uploads/RasterData/*"
delete_rasters = "sudo rm rasters/*"
delete_optimized_rasters = "sudo rm ../../../services/terracotta/optimized-rasters/*"
restart_terracotta = "sudo systemctl restart terracotta"

subprocess.call(delete_media, shell=True)
subprocess.call(delete_rasters, shell=True)
subprocess.call(delete_optimized_rasters, shell=True)
subprocess.call(restart_terracotta, shell=True)


