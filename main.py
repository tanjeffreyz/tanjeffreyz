import json
from src.config import *
from src import utils
from src.settings import SETTINGS


# Overview banner
result = [
    '<div align="center">',
    utils.image(f'{HOST}/overview', GITHUB_STATISTICS, BANNER_WIDTH)
]

# Gather repository info
repos = [[]]
r = 0
c = 0

with open('config.json', 'r') as file:
    config = json.load(file)

    # Parse settings
    if 'settings' in config:
        for key, value in config['settings'].items():
            key = key.lower()
            value = value.lower()
            if key in SETTINGS:
                if value in SETTINGS[key].allowed_values:
                    SETTINGS[key].value = value
                else:
                    print(f" !  Invalid value '{value}' for setting '{key}':")
                    print(' ' * 4 + f' -  Valid values are: {SETTINGS[key].allowed_values}')
            else:
                print(f" !  Unrecognized setting '{key}'")

    for repo in config['items']:
        # Add repo to grid
        if r == len(repos):
            repos.append([])
        repos[r].append((
            repo['owner'].strip(),
            repo['repo'].strip(),
            repo['link'].strip() if 'link' in repo else ''
        ))

        next_c = c + 1
        c = next_c % NUM_COLS
        r += next_c // NUM_COLS

for row in repos:
    if len(row) != NUM_COLS:
        n = len(config['items'])
        print(f"[!] {n} repositories not enough to make {len(repos)}x{NUM_COLS} grid")
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
            src += f"&{s}={SETTINGS[s].value}"
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
