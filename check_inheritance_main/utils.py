import requests
import json
import os
from datetime import datetime
from config import TOKEN, OWNER, REPO, BRANCH 

def get_branch_creation_time(branch_name, prev_alert):
    """Получает время создания комита."""
    response = requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/commits/{prev_alert}', auth=(OWNER, TOKEN))

    if response.status_code == 200:
        commit_info = response.json()
        created_at = commit_info['commit']['committer']['date']
        return datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    else:
        raise Exception(f"Error commit: {response.status_code}")
 
def get_main_branch_sha(owner, repo, token):
    """Получает SHA основной ветки."""
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/branches/main", auth=(owner, token))
    if response.status_code == 200:
        return response.json()['commit']['sha']
    else:
        raise Exception("Error main branch")

def get_all_branches(owner, repo, token):
    """Получает все ветки репозитория."""
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/branches", auth=(owner, token))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Не удалось получить ветки")

def get_commit_parents(commit_sha, owner, repo, token):
    """Получает родителей коммита по его SHA."""
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}", auth=(owner, token))
    if response.status_code == 200:
        return response.json().get('parents', [])
    else:
        raise Exception("Не удалось получить данные коммита")

def load_commits_from_file(filename):
    """Загружает коммиты из JSON файла."""
    with open(filename, 'r') as file:
        return json.load(file)

def save(data, filename):
    """Сохраняет в JSON файл."""
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_alert_commits(filename='alert_commits.json'):
    """Загружает подозрительные коммиты из JSON файла."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

def collect_commits(branches, main_commit_sha, owner, repo, token):
    """Собирает коммиты для каждой ветки."""
    all_commits = {}
    for branch in branches:
        print(f"Branch Name: {branch['name']}")
        all_commits[branch['name']] = []
        current_commit_sha = branch['commit']['sha']
        
        while True:
            if current_commit_sha == main_commit_sha:
                break

            all_commits[branch['name']].append(current_commit_sha)
            parents = get_commit_parents(current_commit_sha, owner, repo, token)
            if parents:
                current_commit_sha = parents[0]['sha']
            else:
                break

    return all_commits