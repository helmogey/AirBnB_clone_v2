#!/usr/bin/python3
# script that generates a .tgz archive
import os
import time
import tarfile


def do_pack():
    """Generates a .tgz archive of the web_static folder contents.

    Returns:
        str: The path to the created archive if successful, None otherwise.
    """

    # Create the "versions" folder if it doesn't exist
    versions_dir = os.path.join(os.getcwd(), "versions")
    if not os.path.exists(versions_dir):
      os.makedirs(versions_dir)

    # Get current date and time for archive name
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = os.path.join(versions_dir, archive_name)

    try:
      # Create the archive
      with tarfile.open(archive_path, "w:gz") as tar:
        # Add all files from web_static recursively (including subdirectories)
        web_static_dir = os.path.join(os.getcwd(), "web_static")
        tar.add(web_static_dir, arcname=os.path.basename(web_static_dir))  # Avoid redundant path

      return archive_path

    except Exception as e:
      print(f"Error creating archive: {e}")
      return None
