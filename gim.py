#!/usr/bin/env python3
import os, sys, json, subprocess

GIT_IM_FILE = ".gim"
GIT_IM_CONFIG = "~/.local/gim/gim.json"

global_config = {}
project_config = {}
project_config_path = ""

#Try to read the global configuration file
if not os.path.exists(os.path.expanduser(GIT_IM_CONFIG)):
    print("Global gim configuration file not found. Gim is quitting: " + GIT_IM_CONFIG)
    sys.exit(1)
else:
    with open(os.path.expanduser(GIT_IM_CONFIG), 'r') as f:
        global_config = json.load(f)

#check if we should run the configuration.
if len(sys.argv) >= 3 and sys.argv[1] == "--gim-init":
    identity_name = sys.argv[2]
    if "identities" not in global_config:
        print("No identities section found in global configuration.")
        sys.exit(1)
    if identity_name not in global_config["identities"]:
        print("Identity not found in global configuration: " + identity_name)
        sys.exit(1)
    #Write the global configuration anconfigure git for this directory
    if os.path.exists(GIT_IM_CONFIG):
        print(f"Project configuration already exists! If you wish to reinitialize it, delete {GIT_IM_FILE} and try again." )
        sys.exit(1)
    else:
        with open(GIT_IM_FILE, 'w') as f:
            new_config = {
                "identity" : identity_name
            }
            json.dump(new_config, f)
        user_name = global_config["identities"][identity_name]["user.name"]
        user_email = global_config["identities"][identity_name]["user.email"]
        r1 = subprocess.run(["git", "config", "user.name", user_name])
        r2 = subprocess.run(["git", "config", "user.email", user_email])
        if r1.returncode != 0 or r2.returncode != 0:
            print("Warning: git configuration failed. If you have not yet initialized this repo, you may need to manually configure git after you do so.")
        print(f"Project initialization complete. Successfully wrote project seettings to \"{GIT_IM_FILE}\"")
        sys.exit(0)

#Before doing anything else, try to read the project configuration.
#We will walk the file system upwards from the current directory, stopping when we find the
#.gim file.
path_split = os.path.realpath(".").split(os.path.sep)
for i in range(len(path_split),0,-1):
    #Gets the current drive /  fs root
    root = "".join(os.path.splitroot(os.path.realpath("."))[:2])
    cur_path = os.path.join(root, *path_split[:i])
    file_path = os.path.join(cur_path, GIT_IM_FILE)
    if cur_path == root:
        #We walked all the way up and faield to find the configuration
        print("gim walked to the top of the file system without finding a configuration for this project.")
        print("Did you create a .gim file by initializing this repo (--gim-init)?")
        sys.exit(1)
        break
    if os.path.exists(file_path):
        project_config_path = file_path
        with open(file_path, 'r') as f:
            project_config = json.load(f)
        break
    elif os.path.exists(".git"):
        #We made it to a top level directory with a .git file, so we should stop before walking all the way up
        #The FS.
        print("Failed to find a configuration for this project. Did you create a .gim file (--gim-init)?")
        sys.exit(1)
else:
    print("Failed to find a configuration for this project. Did you create a .gim file (--gim-init)?")
    sys.exit(1)

#If we've made it here, both configuration files have loaded correctly.
#Before going any further, ensure both the email and username are correct.

project_identity_name = project_config["identity"]
project_identity = global_config["identities"][project_identity_name]

#These checks are skipped for the "git clone" command so that a particular 
#identity may be used while cloning by placing a .gim file in the directory you are cloning into
if not (len(sys.argv) >= 1 and sys.argv[1] == "clone"):
    ret = subprocess.run(["git", "config", "user.email"], capture_output=True)
    if (ret.stdout.decode().strip() != project_identity["user.email"]):
        print(f"The email configured in git ({ret.stdout.decode().strip()}) does not match the email in the identity for this project.")
        print(f"You might correct this by configuring it in git with \"git config user.email {project_identity["user.email"]}\"")
        sys.exit(1)
    ret = subprocess.run(["git", "config", "user.name"], capture_output=True)
    if (ret.stdout.decode().strip() != project_identity["user.name"]):
        print(f"The user name ({ret.stdout.decode().strip()}) configured in git does not match the email in the identity for this project.")
        print(f"You might correct this by configuring it in git with \"git config user.name {project_identity["user.name"]}\"")
        sys.exit(1)

#Ensure that the identity file actually exists and is a valid path
if not os.path.exists(os.path.expanduser(project_identity["privateKey"])):
    print(f"The configured key file for {project_identity_name} could not be located.")
    sys.exit(1)

#Everything seems good up to this point. We can now actually run git.
envrionment_str = f"GIT_SSH_COMMAND=\"ssh -o IdentitiesOnly=yes -i {project_identity["privateKey"]}\""
cmd_str = ' '.join(sys.argv[1:])
print(f"Gim is using the identity: {project_identity_name}")
os.system (envrionment_str + " git " + cmd_str)