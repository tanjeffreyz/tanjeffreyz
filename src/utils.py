IGNORED_TAGS = ('meta', 'link', '!DOCTYPE', 'br', 'hr')


def image(src, link, width):
    return f'<a href="{link}"><img src="{src}" width="{width:.2f}%" /></a>'


def indent(contents):
    """Mutatively indents each line in CONTENTS."""

    curr_indent = 0
    for i in range(len(contents)):
        line = contents[i]
        next_indent = curr_indent
        if not any(line.startswith(f'<{x}') for x in IGNORED_TAGS):
            first = True
            for j in range(len(line)):
                if line[j] == '<':
                    if j < len(line) - 1 and line[j + 1] == '/':
                        if first:
                            curr_indent -= 1  # If '</' comes first, decrease current indent
                        next_indent -= 1
                    else:
                        next_indent += 1
                    first = False
                elif line[j] == '/' and j < len(line) - 1 and line[j + 1] == '>':
                    next_indent -= 1
        contents[i] = ' ' * 4 * max(0, curr_indent) + line
        curr_indent = next_indent
