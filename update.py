import re
import math


DELIMITERS = '/|,'
SETTINGS = {
    'order': [
        '',                 # Default value of setting
        {'zig-zag'}         # Allowed values
    ]
}

# Load template
with open('template.txt', 'r') as file:
    result = [file.read()]

# Gather repository info
repos = []
r = 0
c = 0
with open('repositories.csv', 'r') as file:
    # reader = csv.reader(file, delimiter='/', skipinitialspace=True)
    reader = iter(file.readlines())

    # Retrieve dimensions
    try:
        first_line = next(reader)
        first_line = re.split(DELIMITERS, first_line)
        MAX_ROWS = int(first_line[0].strip())
        MAX_COLS = int(first_line[1].strip())
    except (StopIteration, ValueError):
        print('\n[!] Missing arguments on line 1, expected: MAX_ROWS and MAX_COLS')
        exit()

    # Parse csv
    for i, line in enumerate(reader):
        line = re.split(DELIMITERS, line)
        header = f' !  Line {i}: '
        if len(line) == 2:
            if line[0].startswith('$'):
                key = line[0][1:].strip().lower()
                value = line[1].strip().lower()
                if key in SETTINGS:
                    if value in SETTINGS[key][1]:
                        SETTINGS[key][0] = value
                    else:
                        print(header + f"Invalid value '{value}' for setting '{key}':")
                        print(' ' * 4 + f' -  Valid values are: {SETTINGS[key][1]}')
                else:
                    print(header + f"Unrecognized setting '{key}'")
            else:
                owner = line[0].strip()
                repo = line[1].strip()
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
    for s in SETTINGS:
        src += f"&{s}={SETTINGS[s][0]}"
    link = f'https://github.com/{owner}/{repo}'
    result.append(f'[![]({src})]({link})')
result.append('')

# Update README.md
with open('README.md', 'w') as file:
    file.write('\n'.join(result))
