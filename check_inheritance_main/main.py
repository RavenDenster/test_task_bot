import requests
import json
import os
from datetime import datetime
from config import TOKEN, OWNER, REPO, BRANCH 
from utils import get_branch_creation_time, get_main_branch_sha, get_all_branches, get_commit_parents, load_commits_from_file, save, load_alert_commits, collect_commits


def find_alert_commit(all_commits):
    """Поиск подозрительных коммитов"""
    alert_commit = ''
    for branch_name, commits in all_commits.items():
        for commit in all_commits[BRANCH]:
            if commit in commits and BRANCH != branch_name:
                alert_commit = commit
                break
    return alert_commit

def check_old_alert_commits(alert_commit, alert_origin_commits):
    """Проверяет, существует ли alert_commit в старых ветках"""
    is_alert_commit = None
    for branch_name, commits in alert_origin_commits.items():
        if alert_commit in commits:
            is_alert_commit = (branch_name != BRANCH)
            return is_alert_commit
    return None

def get_matching_branches_and_commits(tail_alert_commit, all_commits):
    """Формирует список подозрительных веток и комитов"""
    matching_branches = [BRANCH]

    for branch_name, commits in all_commits.items():
        if branch_name != BRANCH:
            matching_commits = set(tail_alert_commit) & set(commits)
            if matching_commits:
                matching_branches.append(branch_name)
                print(f"Ветка '{branch_name}' содержит совпадающие коммиты: {matching_commits}")
    if len(matching_branches) > 1:
        common_commits = all_commits[matching_branches[0]]
        for branch in matching_branches[1:]:
            common_commits = [commit for commit in common_commits if commit in all_commits[branch]]
        if common_commits:
            new_alert_commit = common_commits[0] 
            
    return matching_branches, new_alert_commit

def time_comparison(matching_branches, all_commits, alert_commit, new_alert_commit, prev_alert):
    """Сравнение времени создания первых коммитов после общего хвоста"""
    time_create_matching_branch = {}
    trig_end = False

    for branch in matching_branches:
        if branch != BRANCH:
            index_alert_other = (all_commits[branch].index(alert_commit) if len(matching_branches) <= 1 else all_commits[branch].index(new_alert_commit))
            if index_alert_other == 0:
                trig_end = True

            prev_alert_other = all_commits[branch][index_alert_other - 1]
            branch_time = get_branch_creation_time(branch, prev_alert_other)
            time_create_matching_branch[branch] = branch_time
            continue

        if len(matching_branches) <= 1:
            branch_time = get_branch_creation_time(branch, prev_alert)
        else:
            new_index_alert = all_commits[branch].index(new_alert_commit)
            new_prev_alert = all_commits[branch][new_index_alert - 1]
            branch_time = get_branch_creation_time(branch, new_prev_alert)

        time_create_matching_branch[branch] = branch_time

    return time_create_matching_branch, trig_end

def check_branch_from_main(all_commits, alert_origin_commits):
    """Проверяет от какой ветки наследуется текущая ветка."""
    alert_commit = find_alert_commit(all_commits)
    tail_alert_commit = []
    current_branch = all_commits[BRANCH]

    if not alert_commit or len(current_branch) <= 1:
        return False, alert_commit

    value = check_old_alert_commits(alert_commit, alert_origin_commits)
    if value is not None:
        return value, alert_commit

    index_alert = current_branch.index(alert_commit)
    tail_alert_commit = current_branch[index_alert:]
    prev_alert = current_branch[index_alert - 1] if len(current_branch) > 1 and index_alert - 1 != -1 else None

    if prev_alert == None:
        return False, alert_commit
    
    matching_branches, new_alert_commit = get_matching_branches_and_commits(tail_alert_commit, all_commits)
    time_create_matching_branch, trig_end = time_comparison(matching_branches, all_commits, alert_commit, new_alert_commit, prev_alert)
    if trig_end:
        return True, alert_commit
    
    branch_creation_time = time_create_matching_branch[BRANCH]
    return any(branch_creation_time < time_create_matching_branch[branch] for branch in matching_branches if branch != BRANCH), alert_commit


def main():
    filename = 'all_commits.json'
    main_commit_sha = get_main_branch_sha(OWNER, REPO, TOKEN)
    branches = get_all_branches(OWNER, REPO, TOKEN)
    
    with open("branches.json", "w") as file:
        json.dump(branches, file, indent=2)

    if os.path.exists(filename):
        all_commits = load_commits_from_file(filename)
        print("Коммиты загружены из файла")
    else:
        all_commits = collect_commits(branches, main_commit_sha, OWNER, REPO, TOKEN)

        with open("all_commits.json", "w") as file:
            json.dump(all_commits, file, indent=2)

    alert_origin_commits = load_alert_commits()
    if BRANCH not in alert_origin_commits:
        alert_origin_commits[BRANCH] = [] 

    value, alert_commit = check_branch_from_main(all_commits, alert_origin_commits)

    if value:
        print("Ветка создана не от мейна")
    else:
        if alert_commit and alert_commit not in alert_origin_commits[BRANCH]:
            alert_origin_commits[BRANCH].append(alert_commit)
        print("Ветка создана от мейна")

    save(alert_origin_commits, 'alert_commits.json')

if __name__ == "__main__":
    main()
