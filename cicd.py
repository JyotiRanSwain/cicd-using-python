import os
import shutil
import paramiko
import git

def fetch_and_merge(repo_path):
    try:
        # Change directory to the repository path
        os.chdir(repo_path)
        # Open the repository
        repo = git.Repo(repo_path)
        # Fetch changes from the remote repository
        repo.remotes.origin.fetch()
        # Merge fetched changes into the local repository
        repo.git.merge("origin/main")
        print("Fetched changes and merged successfully.")
    except Exception as e:
        print(f"Error fetching and merging changes: {e}")

def maven_clean_package(directory):
    os.chdir(directory)
    os.system('mvn clean package -Dmaven.test.skip=true')

if __name__ == "__main__":
    # GitHub repository URL
    repo_url = "https://github.com/JyotiRanSwain/Powercloud.git"
    
    # Local path to store the repository
    local_path = "D:/bat/Powercloud"

    # Fetch changes from the GitHub repository and merge them
    fetch_and_merge(local_path)

    # Build the project
    maven_clean_package(local_path)

def scp_file(source_path, destination_path, key_path):
    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Load private key
        private_key = paramiko.RSAKey.from_private_key_file(key_path)

        # Connect to the server
        ssh.connect(hostname='54.169.28.71', username='ec2-user', pkey=private_key)

        # SCP the file
        with ssh.open_sftp() as sftp:
            sftp.put(source_path, destination_path)

        print("File transferred successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the SSH connection
        ssh.close()

# Example usage
source_path = 'D:/bat/Powercloud/web/target/Power-Cloud-1.war'
destination_path = '/opt/tomcat/webapps/Power-Cloud-1.war'
key_path = 'D:/bat/build/Powercloud/web/target/office_sing.pem'

scp_file(source_path, destination_path, key_path)
