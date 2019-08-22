#!/usr/bin/python
"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough code, badly documented. Send me comments and patches."""

__author__ = 'Aaron Swartz <me@aaronsw.com>'
__copyright__ = '(C) 2003 Aaron Swartz. GNU GPL 2 or 3.'
__version__ = '0.22'

import difflib, string

def isTag(x):
    return x[0] == "<" and x[-1] == ">"


def html2list(html, brackets=0):
    mode = 'char'
    current_str = ''
    result = []
    for char in html:
        if mode == 'tag':
            if char == '>':
                if brackets:
                    current_str += ']'
                else:
                    current_str += char
                result.append(current_str)
                current_str = ''
                mode = 'char'
            else:
                current_str += char
        elif mode == 'char':
            if char == '<':
                result.append(current_str)
                if brackets:
                    current_str = '['
                else:
                    current_str = char
                mode = 'tag'
            elif char in string.whitespace:
                result.append(current_str + char);
                current_str = ''
            else:
                current_str += char
    result.append(current_str)
    return result


def textDiff(html1, html2, added_class='green', added_element='font', removed_class='red', removed_element='font', moved_class='orange', moved_element='font'):
    out = []
    html1, html2 = html2list(html1), html2list(html2)
    try:
        s = difflib.SequenceMatcher(None, html1, html2, autojunk=False)
    except TypeError:
        s = difflib.SequenceMatcher(None, html1, html2)
    for e in s.get_opcodes():
        if e[0] == "replace":
            out.append(f'<{removed_element} style="color:{removed_class}">' + ''.join(html1[e[1]:e[2]]) + f'</{removed_element}><{added_element} style="color:{added_class}">'+''.join(html2[e[3]:e[4]]) + f'</{added_element}>')
        elif e[0] == "delete":
            out.append(f'<{removed_element} style="color:{removed_class}">' + ''.join(html1[e[1]:e[2]]) + f'</{removed_element}>')
        elif e[0] == "insert":
            out.append(f'<{added_element} style="color:{added_class}">' + ''.join(html2[e[3]:e[4]]) + f'</{added_element}>')
        elif e[0] == "equal":
            if e[1] != e[3] or e[2] != e[4]:
                out.append(f'<{moved_element} style="color:{moved_class}">' + ''.join(html2[e[3]:e[4]]) + f'</{moved_element}>')
            else:
                out.append(''.join(html2[e[3]:e[4]]))
        else:
            raise "Um, something's broken. I didn't expect a '" + e[0] + "'."
    return ''.join(out)
