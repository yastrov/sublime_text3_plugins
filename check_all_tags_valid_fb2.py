# -*- coding: utf-8 -*-
"""Plugin for Sublime Text 3 that check all tags of document are in FB2 standart.
"""

__license__ = "MIT"

import sublime
import sublime_plugin
import re

valid_fb2_tags = {'sequence', 'id', 'td', 'binary', 'book-name', 'src-title-info',
                  'body', 'first-name', 'empty-line/', 'src-lang', 'emphasis',
                  'coverpage', 'subtitle', 'book-title', 'nickname', 'title',
                  'title-info', 'text-author', 'image', 'image/', 'publish-info', 
                  'history', 'city', 'poem', 'epigraph', 'genre', 'tr', 
                  'author', 'version', 'middle-name', 'translator', 'cite', 
                  '?xml', 'table', 'image', 'src-ocr', 'src-url', 'v', 'email',
                  'th', 'year', 'program-used', 'strong', 'document-info', 'a',
                  'last-name', 'sup', 'p', 'section', 'description', 'strikethrough',
                  'stanza', 'keywords', 'custom-info', 'lang', 'FictionBook', 'date',
                  'code', 'sub', 'publisher', 'annotation'}


class Stack(object):
    """LIFO stack"""

    def __init__(self):
        self._items = []

    def is_empty(self):
        return len(self._items) == 0

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def pop_or_none(self):
        if self.is_empty():
            return None
        return self.pop()

    def peek(self):
        return self._items[len(self._items)-1]

    def peek_or_none(self):
        if self.is_empty():
            return None
        return self.peek()

    def size(self):
        return len(self._items)

    def __str__(self):
        return '.'.join(self._items)


class CheckAllTagsValidFb2Command(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        reobj = re.compile("<(\/?[^<>]+)>", re.MULTILINE)
        stack = Stack()
        # Clear selection
        sel = view.sel()
        sel.clear()

        for selected_region in self.selections(view):
            for region in view.lines(selected_region):
                str_buffer = view.substr(region)
                for tag_match in reobj.finditer(str_buffer):
                    tag_current = tag_match.group(1)
                    tag_current = self.extract_only_tag_name(tag_current)
                    if tag_current.startswith('/'):
                        # End (close) tag
                        tag_current = tag_current[1:]
                        stored_tag = stack.peek_or_none()
                        if tag_current != stored_tag:
                            sel.clear()
                            sel.add(region)
                            view.show(sel)
                            view.show_popup('Unfinished tag: "{}" here! Current tag seq: {}'.format(stored_tag, str(stack)))
                            sublime.status_message('Find unfinished tag: "{}"! Current tag seq: {}'.format(stored_tag, str(stack)))
                            return
                        else:
                            # Correct: close opened tag
                            stack.pop()
                    else:
                        if tag_current.endswith('/'):
                            continue
                        # Start tag open
                        stack.push(tag_current)
                    # Check for valid
                    if not tag_current in valid_fb2_tags:
                        sel.clear()
                        sel.add(region)
                        view.show(sel)
                        msg = 'Invalid fb2 tag: "{}" Current seq: {}'.format(tag_current, str(stack))
                        print(msg)
                        view.show_popup('Invalid fb2 tag: "{}"'.format(tag_current))
                        sublime.status_message(msg)
                        return
        sublime.status_message('All tags are in Fb2 standart!')

    def selections(self, view, default_to_all=True):
        """
        Written by Jon LaBelle (jonlabelle)
        From: https://github.com/jonlabelle/Trimmer
        """
        regions = [r for r in view.sel() if not r.empty()]
        if not regions and default_to_all:
            regions = [sublime.Region(0, view.size())]
        return regions

    def extract_only_tag_name(self, tag):
        _tag = tag
        pos = tag.find(' ')
        if pos > 0:
            _tag = tag[:pos]
        if tag.endswith('/') and not _tag.endswith('/'):
            _tag = '{}/'.format(_tag)
        return _tag
