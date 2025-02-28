#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import os
import datetime

rank_history_folder = 'rank_history'
total_stars_list = []
total_forks_list = []
today = datetime.datetime.today()

# Try current year first, if no data found, use previous year
current_year = today.year
file_name_start = f'esp_rank_{current_year}-01-01.md'
file_name_end = f'esp_rank_{today.strftime("%Y-%m-%d")}.md'

# If no files found in current year, check previous year
if not os.path.exists(os.path.join(rank_history_folder, file_name_start)):
    current_year = today.year - 1
    file_name_start = f'esp_rank_{current_year}-01-01.md'
    file_name_end = f'esp_rank_{current_year}-12-31.md'

file_name_next = file_name_start

while file_name_next <= file_name_end:
    if not os.path.exists(os.path.join(rank_history_folder, file_name_next)):
        current_date = datetime.datetime.strptime(file_name_next.split('_')[-1].split('.')[0], '%Y-%m-%d')
        file_name_next = f'esp_rank_{(current_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")}.md'
        continue
        
    with open(os.path.join(rank_history_folder, file_name_next), 'r') as readme_file:
        for line in readme_file:
            if 'Total Star 🌟:' in line:
                total_star = int(line.split('Total Star 🌟: ')[1].split(',')[0])
                total_fork = int(line.split('Total Fork 🌳: ')[1].split(',')[0])
                break
        total_stars_list.append(total_star)
        total_forks_list.append(total_fork)
    
    current_date = datetime.datetime.strptime(file_name_next.split('_')[-1].split('.')[0], '%Y-%m-%d')
    file_name_next = f'esp_rank_{(current_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")}.md'

# Check if we have data before proceeding
if not total_stars_list or not total_forks_list:
    print(f"No data found for year {current_year}")
    exit(0)

# Calculate the increase of Total Star, Total Fork
increase_stars = total_stars_list[-1] - total_stars_list[0]
increase_stars_rate = increase_stars / total_stars_list[0] * 100
increase_forks = total_forks_list[-1] - total_forks_list[0]
increase_forks_rate = increase_forks / total_forks_list[0] * 100

# Draw graphs
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(total_stars_list, color='orange')
plt.title('Total Star\nFrom ' + file_name_start.split('_')[1].split('.')[0] + 
          ' to ' + file_name_end.split('_')[1].split('.')[0])
plt.xlabel('Days')
plt.ylabel('Total Star')
plt.text(len(total_stars_list) - 1, total_stars_list[-1], 
         f'+{increase_stars}\n({round(increase_stars_rate, 2)}%)', 
         fontsize=10, color='red', ha='left')

plt.grid()
plt.subplot(1, 2, 2)
plt.plot(total_forks_list, color='blue')
plt.title('Total Fork\nFrom ' + file_name_start.split('_')[1].split('.')[0] + 
          ' to ' + file_name_end.split('_')[1].split('.')[0])
plt.xlabel('Days')
plt.ylabel('Total Fork')
plt.text(len(total_forks_list) - 1, total_forks_list[-1], 
         f'+{increase_forks}\n({round(increase_forks_rate, 2)}%)', 
         fontsize=10, color='red', ha='left')

plt.grid()

# save the graph to stats folder
if not os.path.exists('stats'):
    os.makedirs('stats')
plt.savefig(os.path.join('stats', f'stats_total_star_fork_{current_year}.png'))