import requests
import os
import shutil

GITHUB_REPO = 'petervislocky/weatherApp'

def get_latest_release():
    url = f'https://api.github.com/repos/{GITHUB_REPO}/releases/latest'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def download_asset(asset_url, download_path):
    response = requests.get(asset_url, stream=True)
    response.raise_for_status()
    with open(download_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def update():
    release_info = get_latest_release()
    asset = release_info['assets'][0]
    asset_url = asset['browser_download_url']
    asset_name = asset['name']

    # Get the dir of the currently running script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(current_dir, asset_name)

    print(f'Downloading {asset_name} from {asset_url}...')
    download_asset(asset_url, download_path)

    print(f'Moving {asset_name} to the application directory...')
    app_dir = os.path.dirname(current_dir)
    shutil.move(download_path, os.path.join(app_dir, asset_name))

    print('Update complete!')

if __name__ == '__main__':
    update()