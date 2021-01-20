#!/usr/bin/env python3
import os
import sys
import bibtexparser
import yaml

ROOT = os.path.abspath(os.path.dirname(__file__))
WEB_DIR = os.path.join(ROOT, "../web")

sys.path.insert(0, os.path.join(WEB_DIR, 'bin'))
import make as web

def tex_highlight(s):
    return "\\textbf{%s}" % s

LB = ' \\\\'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: %s output_path' % sys.argv[0])
        sys.exit(-1)

    conf_dict, pub_entries = web.read_bib(tex_highlight)
    text = ''
    for entry in pub_entries:
        if 'crossref' in entry:
            conf = conf_dict[entry['crossref']]
        else:
            conf = entry

        if entry['ENTRYTYPE'] == 'phdthesis':
            conf['title'] = 'Ph.D. thesis, %s' % entry['school']

        # XXX: Fix this... so bad design
        entry['author'] = entry['author'].replace('\\*', '*')
        content = ['\\item %s %s' % (tex_highlight(entry['title']), LB),
            '{\\footnotesize',
            '  ' + entry['author'] + LB,
            '  ' + conf['title'] + LB]

        location = ''
        if 'address' in conf:
            location += '%s, ' % conf['address']

        location += '%s %s' % (conf['month'], conf['year'])
        content.append(location)

        if 'award' in entry:
            content[-1] += LB
            content.append('  ' + tex_highlight('$\\bullet$ %s' % entry['award']))

        content += ['}', '']
        text += '\n'.join(content)

    with open(os.path.join(WEB_DIR, "cve.md")) as f:
        entries = []
        entry = {}
        for l in f:
            l = l.strip()
            if not l:
                entries.append(entry)
                entry = {}
            else:
                k, v = l.strip().split(': ', 1)
                k = k.strip()
                v = v.strip()
                if k == 'cve':
                    v = v.split(', ')
                entry[k] = v
        cves = ', '.join(sorted(map(lambda entry: "\\cc{%s}" % entry['cve'][0], entries)))
        cves = cves.replace("#", "\\#")

    with open(os.path.join(ROOT, '../cv.tex')) as f:
        text = web.replace_text(f.read(), 'PUB', text)
        text = web.replace_text(text, 'CVE', cves)

    with open(sys.argv[1], 'w') as f:
        f.write(text)
