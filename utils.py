import json
from os import path, scandir, mkdir
import subprocess
import time
from typing import TypedDict, List

import folder_paths
from comfy.cli_args import args

SERVER_BASE_URL = f'http://{args.listen}:{args.port}'
# To support IPv6
if ':' in args.listen:
    SERVER_BASE_URL = f'http://[{args.listen}]:{args.port}'

browser_path = path.dirname(__file__)
collections_path = path.join(browser_path, 'collections')
config_path = path.join(browser_path, 'config.json')

parent_folder = path.dirname(browser_path)
parent_folder = path.dirname(parent_folder)
sources_path = parent_folder

print("KKKKK --- Parent folder:", parent_folder)

download_logs_path = path.join(browser_path, 'download_logs')
outputs_path = folder_paths.get_output_directory()
if args.output_directory:
    outputs_path = path.abspath(args.output_directory)

for dir in [collections_path, sources_path, download_logs_path, outputs_path]:
    if not path.exists(dir):
        mkdir(dir)


image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp','.safetensors']
video_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv']
white_extensions = ['.json', '.html'] + image_extensions + video_extensions

info_file_suffix = '.info'

git_remote_name = 'origin'

class FileInfoDict(TypedDict):
    type: str
    name: str
    bytes: int
    created_at: float
    folder_path: str
    notes: str

def log(message):
    print('[comfyui-browser] ' + message)

def run_cmd(cmd, run_path, log_cmd=True, log_code=True, log_message=True):
    if log_cmd:
        log(f'running: {cmd}')

    ret = subprocess.run(
        f'cd {run_path} && {cmd}',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="UTF-8"
    )
    if log_code:
        if ret.returncode == 0:
            log('successed')
        else:
            log('failed')
    if log_message:
        if (len(ret.stdout) > 0 or len(ret.stderr) > 0):
            log(ret.stdout + ret.stderr)

    return ret

# folder_type = 'outputs', 'collections', 'sources'
def get_parent_path(folder_type: str):
    if folder_type == 'collections':
        return collections_path
    if folder_type == 'sources':
        return sources_path

    # outputs
    return outputs_path

# folder_type = 'outputs', 'collections', 'sources'
def get_target_folder_files(folder_path: str, folder_type: str = 'outputs'):
    if '..' in folder_path:
        return None

    parent_path = get_parent_path(folder_type)
    files: List[FileInfoDict] = []
    target_path = path.join(parent_path, folder_path)

    if not path.exists(target_path):
        return []

    folder_listing = scandir(target_path)
    folder_listing = sorted(folder_listing, key=lambda f: (f.is_file(), -f.stat().st_ctime))
    for item in folder_listing:
        if not path.exists(item.path):
            continue

        name = path.basename(item.path)
        ext = path.splitext(name)[1].lower()

        created_at = item.stat().st_ctime
        info_file_path = get_info_filename(item.path)
        info_data = {}
        if path.exists(info_file_path):
            with open(info_file_path, 'r') as f:
                info_data = json.load(f)
        if item.is_file():
            bytes = item.stat().st_size
            files.append({
                "type": "file",
                "name": name,
                "bytes": bytes,
                "created_at": created_at,
                "folder_path": folder_path,
                "notes": info_data.get("notes", "")
            })
        elif item.is_dir():
            files.append({
                "type": "dir",
                "name": name,
                "bytes": 0,
                "created_at": created_at,
                "folder_path": folder_path,
                "notes": info_data.get("notes", "")
            })

    return files

def get_info_filename(filename):
    return path.splitext(filename)[0] + info_file_suffix

def add_uuid_to_filename(filename):
    name, ext = path.splitext(filename)
    return f'{name}_{int(time.time())}{ext}'

def get_config():
    if not path.exists(config_path):
        return {}

    with open(config_path, 'r') as f:
        return json.load(f)

def git_init(run_path = collections_path):
    if not path.exists(path.join(run_path, '.git')):
        run_cmd('git init', collections_path)

    ret = run_cmd('git config user.name', collections_path,
                  log_cmd=False, log_code=False, log_message=False)
    if len(ret.stdout) == 0:
        ret = run_cmd('whoami', collections_path,
                      log_cmd=False, log_code=False, log_message=False)
        username = ret.stdout.rstrip("\n")
        run_cmd(f'git config user.name "{username}"', collections_path)

    ret = run_cmd('git config user.email', collections_path,
                  log_cmd=False, log_code=False, log_message=False)
    if len(ret.stdout) == 0:
        ret = run_cmd('hostname', collections_path,
                      log_cmd=False, log_code=False, log_message=False)
        hostname = ret.stdout.rstrip("\n")
        run_cmd(f'git config user.email "{hostname}"', collections_path)
