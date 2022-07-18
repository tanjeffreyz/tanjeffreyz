def get_banner(src, href):
    with open('templates/banner.txt', 'r') as file:
        template = file.read()
        return template.replace('__SRC__', src).replace('__HREF__', href)
