import re
import math
import utils
from config import *


# Overview banner
result = [
    '<div align="center">',
    utils.image(f'{HOST}/overview', GITHUB_STATISTICS, BANNER_WIDTH)
]

# Gather repository info
repos = [[]]
r = 0
c = 0
with open('.config', 'r') as file:
    reader = iter(file.readlines())

    # Parse csv
    for i, line in enumerate(reader):
        line = re.split(DELIMITERS, line)
        header = f' !  Line {i}: '
        if len(line) >= 2:
            if line[0].startswith('$'):
                # Parse setting
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
                # Parse repository
                owner = line[0].strip()
                repo = line[1].strip()
                custom_link = ''.join(x.strip() for x in line[2:])

                # Add repo to grid
                if r == len(repos):
                    repos.append([])
                repos[r].append((owner, repo, custom_link))

                next_c = c + 1
                c = next_c % NUM_COLS
                r += next_c // NUM_COLS

for row in repos:
    if len(row) != NUM_COLS:
        print(f'[!] CRITICAL: Not enough repositories to make {len(repos)}x{NUM_COLS} grid')
        exit(1)


# Create entries
rows = len(repos)
for r in range(rows):
    cols = len(repos[r])
    html_row = []
    for c in range(cols):
        owner, repo, custom_link = repos[r][c]

        src = f'{HOST}/repo?r={r}&c={c}&maxR={rows}&owner={owner}&repo={repo}'
        for s in SETTINGS:
            src += f"&{s}={SETTINGS[s][0]}"
        link = custom_link if custom_link else f'https://github.com/{owner}/{repo}'

        html_row.append(utils.image(src, link, CARD_WIDTH))
    num_spacers = cols - 1
    spacer_size = (BANNER_WIDTH - NUM_COLS * CARD_WIDTH) / num_spacers
    spacer = utils.image(f'{HOST}/spacer', '#', spacer_size)
    result.append(spacer.join(html_row))

# Footer banner
result.append(utils.image(f'{HOST}/footer?maxR={rows}', GITHUB_STATISTICS, BANNER_WIDTH))

# Close div and update README.md
result.append('</div>')
result.append('')
with open('README.md', 'w') as file:
    utils.indent(result)
    file.write('\n'.join(result))
