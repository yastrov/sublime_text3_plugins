import sublime
import sublime_plugin
import re


class Stack(object):
    """LIFO stack"""
    def __init__(self):
        self._items = []
        self._empty = []

    def isEmpty(self):
        return self._items == self._empty

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def pop_or_None(self):
        if self.isEmpty():
            return None
        return self._items.pop()

    def peek(self):
        return self._items[len(self._items)-1]

    def size(self):
        return len(self._items)


class FindBrokenXmlTag(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        reobj = re.compile("<(\/?[^<>]+)>", re.MULTILINE)
        stack = Stack()
        sel = view.sel()
        sel.clear()

        for main_r in self.selections(view):
            for region in view.lines(main_r):
                str_buffer = view.substr(region)
                for each_match in reobj.finditer(str_buffer):
                    tag_current = each_match.group(1)

                    if tag_current.startswith('/'):
                        tag_current = tag_current[1:]
                        stored_tag = stack.pop_or_None()
                        if tag_current != stored_tag:
                            sel.clear()
                            sel.add(region)
                            view.show(sel)
                            #view.show_popup('Error tag: "{} here!'.format(stored_tag))
                            #sublime.status_message('Find error tag: "{}"!!'.format(stored_tag))
                            view.show_popup('Здесь ошибка в тег с именем: "{}" остался открыт!'.format(stored_tag))
                            sublime.status_message('Здесь ошибка в теге с именем: "{}"!!'.format(stored_tag))
                            #flag = False
                            #break
                            return
                    else:
                        stack.push(tag_current)
                #if flag:
                    #break

    def selections(self, view, default_to_all=True):
        regions = [r for r in view.sel() if not r.empty()]
        if not regions and default_to_all:
            regions = [sublime.Region(0, view.size())]
        return regions
