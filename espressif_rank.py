#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'esp'

import sys, json, os, requests, datetime

today = datetime.date.today()
output_message = f'# Espressif Systems Github Star Rank {today}\n\n'
github_id = "espressif"
url = 'https://api.github.com/users/{github_id}/repos?page={page_id}'
repo_list = []
page_id = 1

# Check if README.md exists and save it with a new name if it does
if os.path.isfile('README.md'):
    with open('README.md', 'r') as readme_file:
        first_line = readme_file.readline()
        if 'Espressif Systems Github Star Rank' in first_line:
            old_date = first_line.split()[-1]
            new_filename = f'esp_rank_{old_date}.md'
            os.rename('README.md', new_filename)
            print(f'Previous README.md saved as {new_filename}.')

            # Move the previous file to the 'rank_history' folder
            rank_history_folder = 'rank_history'
            if not os.path.exists(rank_history_folder):
                os.makedirs(rank_history_folder)
            os.rename(new_filename, os.path.join(rank_history_folder, new_filename))
            print(f'{new_filename} moved to {rank_history_folder} folder.')

while True:
    r = requests.get(url.format(github_id=github_id, page_id=page_id))
    if r.status_code != 200:
        print('check your network connections')
        exit()

    repo_array = json.loads(r.content.decode('utf-8'))
    if len(repo_array) == 0:
        break

    for repo in repo_array:
        if not repo['fork']:
            repo_list.append([repo['name'], repo['stargazers_count'], repo['forks_count'], repo['description'], repo['html_url']])
    page_id += 1

# sort by number of stars
repo_list = sorted(repo_list, key=lambda x: x[1], reverse=True)

total_stars = sum([i[1] for i in repo_list])
total_forks = sum([i[2] for i in repo_list])

output_message += f'## Total Star 🌟: {total_stars}, Total Fork 🌳: {total_forks}\n\n'
output_message += '[![Update Espressif Systems Github Star Rank](https://github.com/leeebo/espressif_star_counter/actions/workflows/update_rank.yml/badge.svg)](https://github.com/leeebo/espressif_star_counter/actions/workflows/update_rank.yml)\n\n'
output_message += f'![](stats/stats_total_star_fork_' + str(today.year) + '.png)\n\n'
output_message += '| Repository | Stars | Forks | Description |\n'
output_message += '|------------|-------|-------|-------------|\n'
for repo in repo_list:
    output_message += f"| [{repo[0]}]({repo[4]}) | {repo[1]} | {repo[2]} | {repo[3]} |\n"

# Save the output to README.md
with open('README.md', 'w') as readme_file:
    readme_file.write(output_message)

print("Markdown table saved to README.md.")
