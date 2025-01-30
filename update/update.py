import requests
import os
import shutil
import sys
import subprocess

GITHUB_REPO = 'petervislocky/weatherApp'

def get_latest_release():
    url = f'https://api.github.com/repos/{GITHUB_REPO}/releases/latest'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def download_asset(asset_url, download_path):
    try:
        response = requests.get(asset_url, stream=True)
        response.raise_for_status()
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        with open(download_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Successfully downloaded {download_path}')
    except Exception as e:
        print(f'Failed to download {asset_url}: {e}')
        return False
    return True

def update():
    release_info = get_latest_release()
    asset = release_info['assets'][0]
    asset_url = asset['browser_download_url']
    asset_name = asset['name']

    # Get the dir of the currently running script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(current_dir, asset_name)

    print(f'Current directory: {current_dir}')
    print(f'Downloading {asset_name} from {asset_url} to {download_path}...')
    if not download_asset(asset_url, download_path):
        print('Update failed: Could not download the update file.')
        return

    if not os.path.exists(download_path):
        print('Update failed: Downloaded file does not exist.')
        return

    # Determine the path to the original executable
    if getattr(sys, 'frozen', False):
        # If running as a bundled executable
        original_executable = sys.executable
    else:
        # If running as a script
        original_executable = os.path.join(os.path.dirname(current_dir), asset_name)

    print(f'Preparing to move {asset_name} to the application directory...')
    print(f'Original executable: {original_executable}')
    print(f'Downloaded executable: {download_path}')

    # Create a batch script to replace the executable after the application exits
    batch_script = os.path.join(current_dir, 'update.bat')
    with open(batch_script, 'w') as f:
        f.write(f'@echo off\n')
        f.write(f'ping 127.0.0.1 -n 5 > nul\n')  # Wait for 5 seconds
        f.write(f'move /Y "{download_path}" "{original_executable}"\n')
        f.write(f'start "" "{original_executable}"\n')
        f.write(f'del "%~f0"\n')  # Delete the batch script itself

    print(f'Executing batch script: {batch_script}')
    subprocess.Popen(batch_script, shell=True)
    sys.exit(0)

if __name__ == '__main__':
    update()