import re


def clean_list(
        data: list,
) -> list:
    clean_users = []

    for item in data:  # Skip the first item (usually metadata or header)
        item = item.strip()  # Remove leading/trailing spaces
        item = item.replace("(Feed)", "").strip()  # Remove "(Feed)" and extra spaces

        # Stop processing when the string starts with 'All users were found at'
        if item.startswith("All users were found at"):
            break

        clean_users.append(item)

    return clean_users


def save_as_dict(
        data: str,
) -> dict:
    obj = {}
    in_match = False  # Flag to track if we're inside the Match(s) section
    match_values = []

    for line in data.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            transformed_key = key.strip().replace(' ', '_').lower().strip()

            # Check for 'Match(s):' to begin collecting subsequent lines
            if 'Match(s):' in line:
                in_match = True
            else:
                if in_match:
                    # If we were collecting match values and encounter a new key, stop and add the collected values
                    obj['match_values'] = match_values
                    in_match = False
                obj[transformed_key] = value.strip()
        elif in_match:
            line = line.strip()
            if line:
                match_values.append(line)

    if match_values:
        obj['match_values'] = match_values
    return obj


def edit(data: str):
    result = {}

    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    # Remove ANSI escape codes
    data = ansi_escape.sub('', data)

    plugins = []
    themes = []

    out = data[data.find('['):]
    # out = remove_color_code(out)
    out = re.split(r'\[?] |\[!] ', out)
    out = list(filter(None, out))
    junk_chars = ['[?', '?', '[!', '[i', '     ', ' |   ', '    ? ', '[✔', '[✗', '— ']
    for c in junk_chars:
        out = [w.replace(c, '') for w in out]
    for el in out:
        if el.find('This target is not running wordpress!') != -1:
            result['result'] = {'no_wp': 'The site doesn\'t use Wordpress.'}
            return result

        if el.find('Web Application Firewall') != -1:
            firewall = save_as_dict(el)
            result['waf'] = firewall

        elif el.find('Firewall Active Detection') != -1:
            firewall = save_as_dict(el)
            result['firewall_active'] = firewall

        elif el.find('WordPress Version:') != -1:
            el = el.split('\n')
            result['wp_version'] = el[1][12:]

        elif el.find('Sitemap.xml found:') != -1:
            el = list(filter(None, re.split(': |\n', el)))
            result['sitemap'] = el[1]

        elif el.find('Robots.txt file text:') != -1:
            el = el.replace('Robots.txt file text:\n', '').replace('|', '').strip()
            el = re.sub(r'\n+', '\n', el)  # Replace multiple newlines with one
            el = re.sub(r'\s{2,}', ' ', el)  # Replace multiple spaces with a single space

            # Strip leading and trailing spaces if necessary
            result['robot_txt'] = el.strip()

        elif el.find('WordPress Users') != -1:
            el = list(filter(None, re.split(': |\n', el)))
            result['wp_users'] = clean_list(el[1:])  # array

        elif el.find('Target information(s):') != -1:
            target = save_as_dict(el.replace('Target information(s):\n', ''))
            result.update(target)

        elif el.find('XML-RPC') != -1:
            xml = save_as_dict(el.replace('XML-RPC Enabled:\n', ''))
            result['xml'] = xml

        elif el.find('Theme: ') != -1:
            el = list(filter(None, re.split(': |\n', el)))
            themes.append(el[1:])

        elif el.find('Plugin: ') != -1:
            plugin = save_as_dict(el)
            result['plugin'] = plugin

    if themes:
        result['themes'] = themes
    if plugins:
        result['plugins'] = plugins

    return result
