#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import os
import datetime

# In order from far to near to open files named with 'esp_rank_YYYY-MM-DD.md in the rank_history folder.
# Count Total Star, Total Fork from line eg."## Total Star 🌟: 58152, Total Fork 🌳: 26609"
# Save the Total Star, Total Fork to the list, then draw the graph using matplotlib
# show the trend of the Total Star, Total Fork
rank_history_folder = 'rank_history'
total_stars_list = []
total_forks_list = []
today = datetime.datetime.today()
file_name_start = 'esp_rank_' + today.strftime('%Y-01-01') + '.md'
file_name_end = 'esp_rank_' + today.strftime('%Y-%m-%d') + '.md'
file_name_next = file_name_start

while file_name_next != file_name_end:
    #check if the file exists, if not, skip to the next day
    if not os.path.exists(os.path.join(rank_history_folder, file_name_next)):
        file_name_next = 'esp_rank_' + (datetime.datetime.strptime(file_name_next.split('_')[-1].split('.')[0], '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d') + '.md'
        continue
    with open(os.path.join(rank_history_folder, file_name_next), 'r') as readme_file:
        for line in readme_file:
            if 'Total Star 🌟:' in line:
                total_star = int(line.split('Total Star 🌟: ')[1].split(',')[0])
                total_fork = int(line.split('Total Fork 🌳: ')[1].split(',')[0])
                break
        total_stars_list.append(total_star)
        total_forks_list.append(total_fork)
    file_name_next = 'esp_rank_' + (datetime.datetime.strptime(file_name_next.split('_')[-1].split('.')[0], '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d') + '.md'

# Calculate the increase of Total Star, Total Fork
increase_stars = total_stars_list[-1] - total_stars_list[0]
increase_stars_rate = increase_stars / total_stars_list[0] * 100
increase_forks = total_forks_list[-1] - total_forks_list[0]
increase_forks_rate = increase_forks / total_forks_list[0] * 100

# Draw two graph, star from the bottom left corner
# show the increase number in the top right corner
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(total_stars_list, color='orange')
plt.title('Total Star'
            '\n'
            'From ' + today.strftime('%Y-01-01') + ' to ' + today.strftime('%Y-%m-%d'))
plt.xlabel('Days')
plt.ylabel('Total Star')
plt.text(len(total_stars_list) - 1, total_stars_list[-1], '+' + str(increase_stars) + '\n(' + str(round(increase_stars_rate, 2)) + '%)', fontsize=10, color='red', ha='left')

plt.grid()
plt.subplot(1, 2, 2)
plt.plot(total_forks_list, color='blue')
plt.title('Total Fork'
            '\n'
            'From ' + today.strftime('%Y-01-01') + ' to ' + today.strftime('%Y-%m-%d'))
plt.xlabel('Days')
plt.ylabel('Total Fork')
plt.text(len(total_forks_list) - 1, total_forks_list[-1], '+' + str(increase_forks) + '\n(' + str(round(increase_forks_rate, 2)) + '%)', fontsize=10, color='red', ha='left')

# save the graph to stats folder
if not os.path.exists('stats'):
    os.makedirs('stats')
plt.savefig(os.path.join('stats', 'stats_total_star_fork_' + today.strftime('%Y') + '.png'))