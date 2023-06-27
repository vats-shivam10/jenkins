import paramiko
import argparse

def grant_access(public_key, private_key, servers, user):
    for server in servers:
        try:
            #Create an SSH client and connect to the server
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(server, username=user, pkey=private_key)

            # Append the public key to the authorized_keys file
            sftp_client = ssh_client.open_sftp()
            authorized_keys_path = '.ssh/authorized_keys'
            authorized_keys = sftp_client.open(authorized_keys_path, 'a')

            # Check if the file is empty
            if sftp_client.stat(authorized_keys_path).st_size != 0:
                authorized_keys.write('\n')  # Add a newline before appending the key

            authorized_keys.write(public_key)
            authorized_keys.close()
            sftp_client.close()

            ssh_client.close()

            print(f"Access granted to server {server}")
        except paramiko.AuthenticationException:
            print(f"Authentication failed for server {server}")
        except paramiko.SSHException as ssh_ex:
            print(f"SSH error occurred for server {server}: {str(ssh_ex)}")
        except Exception as ex:
            print(f"An error occurred for server {server}: {str(ex)}")

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--public-key', help='Public key string')
parser.add_argument('--private-key', help='Path to the private key file')
parser.add_argument('--servers', nargs='+', help='List of servers')
parser.add_argument('--user', help='User')
args = parser.parse_args()

# Check if required arguments are provided
if not args.public_key or not args.private_key or not args.servers:
    parser.error('Missing required arguments')

# Load the private key
private_key = paramiko.RSAKey(filename=args.private_key)

# Grant access to servers
grant_access(args.public_key, private_key, args.servers, args.user)
