import os
import stat
import sys

# Add execute permission to the file for the user.
if __name__ == "__main__":
    script_path = os.path.abspath(sys.argv[0])
    current_permissions = os.stat(script_path).st_mode
    os.chmod(script_path, current_permissions | stat.S_IXUSR)
