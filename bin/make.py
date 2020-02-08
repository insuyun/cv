#!/usr/bin/env python3
import os
import sys
import bibtexparser

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../web/bin'))
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
        conf = conf_dict[entry['crossref']]
        content = ['\\item %s %s' % (tex_highlight(entry['title']), LB),
            '{\\footnotesize',
            '  ' + entry['author'] + LB,
            '  ' + conf['title'] + LB,
            '  %s, %s %s' % (conf['address'], conf['month'], conf['year'])]

        if 'award' in entry:
            content[-1] += LB
            content.append('  ' + tex_highlight('$\\bullet$ %s' % entry['award']))

        content += ['}', '']
        text += '\n'.join(content)

    with open(os.path.join(os.path.dirname(__file__), '../cv.tex')) as f:
        text = web.replace_text(f.read(), 'PUB', text)

    with open(sys.argv[1], 'w') as f:
        f.write(text)
