#!/usr/bin/python3
# script that generates a .tgz archive
from fabric import Connection, env
import os


def do_deploy(archive_path, user, key_filename):
    """Deploys the archive to web servers.

    Args:
        archive_path (str): Path to the archive file.
        user (str): Username for SSH access to the servers.
        key_filename (str): Path to the SSH key file.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """

    # Define web server hosts
    env.hosts = ["34.234.201.238", "54.237.54.236"]
    env.user = user
    env.key_filename = key_filename

    # Check if archive exists
    if not os.path.exists(archive_path):
        print(f"Error: Archive file not found: {archive_path}")
        return False

    # Connect to each web server
    with Connection.parallel() as c:
        for server in c:
            # Upload archive to /tmp/
            try:
                server.put(archive_path, remote='/tmp/')
            except Exception as e:
                print(f"Error uploading archive to {server.host}: {e}")
                return False

            # Extract archive
            archive_filename = os.path.basename(archive_path)
            target_dir = f"/data/web_static/releases/{archive_filename.split('.')[0]}"
            try:
                server.run(f"tar -xzf /tmp/{archive_filename} -C {target_dir}")
            except Exception as e:
                print(f"Error extracting archive on {server.host}: {e}")
                return False

            # Delete archive
            try:
                server.run(f"rm /tmp/{archive_filename}")
            except Exception as e:
                print(f"Error deleting archive on {server.host}: {e}")
                return False

            # Delete symbolic link and recreate it
            try:
                server.run("rm /data/web_static/current", warn=True)  # Suppress warning if link doesn't exist
                server.run(f"ln -s {target_dir} /data/web_static/current")
            except Exception as e:
                print(f"Error creating symbolic link on {server.host}: {e}")
                return False

    print("Deployment successful!")
    return True