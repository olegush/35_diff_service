#!/usr/bin/python
"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough code, badly documented. Send me comments and patches."""

__author__ = 'Aaron Swartz <me@aaronsw.com>'
__copyright__ = '(C) 2003 Aaron Swartz. GNU GPL 2 or 3.'
__version__ = '0.22'

import difflib, string

def isTag(x):
    return x[0] == "<" and x[-1] == ">"

def textDiff(a, b):
    """Takes in strings a and b and returns a human-readable HTML diff."""

    out = ['<style>.red {color:red;} .green {color:green;} .orange {color:orange;}</style>']
    a, b = html2list(a), html2list(b)
    try:
        # autojunk can cause malformed HTML, but also speeds up processing.
        s = difflib.SequenceMatcher(None, a, b, autojunk=False)
    except TypeError:
        s = difflib.SequenceMatcher(None, a, b)
    for e in s.get_opcodes():
        if e[0] == "replace":
            out.append('<font class="red">'+''.join(a[e[1]:e[2]]) + '</font><font class="green">'+''.join(b[e[3]:e[4]])+"</font>")
        elif e[0] == "delete":
            out.append('<font class="red">'+ ''.join(a[e[1]:e[2]]) + "</font>")
        elif e[0] == "insert":
            out.append('<font class="green">'+''.join(b[e[3]:e[4]]) + "</font>")
        elif e[0] == "equal":
            if e[1] != e[3] or e[2] != e[4]:
                out.append('<font class="orange">'+''.join(b[e[3]:e[4]]) + "</font>")
            else:
                out.append(''.join(b[e[3]:e[4]]))
        else:
            raise "Um, something's broken. I didn't expect a '" + e[0] + "'."
    return ''.join(out)

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
