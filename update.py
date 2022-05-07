import csv
import math


# Load template
with open('template.txt', 'r') as file:
    result = [file.read()]

# Gather repository info
repos = []
r = 0
c = 0
with open('repositories.csv', 'r') as file:
    reader = csv.reader(file, delimiter='/', skipinitialspace=True)
    try:
        first_line = next(reader)
        MAX_ROWS = int(first_line[0])
        MAX_COLS = int(first_line[1])
    except (StopIteration, ValueError):
        print('\n[!] Invalid arguments on line 1, expected: MAX_ROWS and MAX_COLS')
        exit()

    for line in reader:
        if len(line) == 2:
            owner, repo = line
            repos.append((owner, repo, r, c))
            incremented_c = c + 1
            c = incremented_c % MAX_COLS
            r += incremented_c // MAX_COLS
            if r >= MAX_ROWS or c >= MAX_COLS:
                break

# Create entries
max_r = math.ceil(len(repos) / MAX_COLS)
for owner, repo, r, c in repos:
    src = f'https://tanjeffreyz-github-overview.herokuapp.com/repo/?r={r}&c={c}&maxR={max_r}&owner={owner}&repo={repo}'
    link = f'https://github.com/{owner}/{repo}'
    result.append(f'[![]({src})]({link})')
result.append('')

# Update README.md
with open('README.md', 'w') as file:
    file.write('\n'.join(result))
