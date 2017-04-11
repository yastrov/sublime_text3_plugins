import sublime
import sublime_plugin

valid_fb2_tags = ['p', 'section', 'empty-line/', 'emphasis', 'strong',
                  'epigraph','cite', 
                  'book-name', 'src-title-info', 'title', 'image', 
                  'image',
                  'v', 'stanza',  'poem',  'text-author',
                  'a', 'body', 'subtitle', 'sup','sub',
                  'id', 'binary', 'src-lang','td',
                  'first-name',
                  'coverpage', 'book-title', 'nickname', 
                  'title-info',  'publish-info', 'sequence', 
                  'history', 'city',  'genre', 'tr', 
                  'author', 'version', 'middle-name', 'translator', 
                  '?xml', 'table',  'src-ocr', 'src-url',  'email',
                  'th', 'year', 'program-used',  'document-info', 
                  'last-name',  'description', 'strikethrough',
                  'keywords', 'custom-info', 'lang', 'FictionBook', 'date',
                  'code', 'publisher', 'annotation']


class Fb2AutoCompleterListener(sublime_plugin.ViewEventListener):
    def on_query_completions(self, prefix, locations):
        """return list, tuple or None"""
        fname = self.view.file_name()
        if fname is None or fname=='' or fname.endswith('.fb2'):
            if prefix.startswith('/'):
                _p = prefix[1:]
                _l = list(['/{}\t{}'.format(s, 'valid fb2 tag'), '/{}>'.format(s)]\
                          for s in \
                          filter(lambda s: s.startswith(_p), valid_fb2_tags)
                         )
                return _l if len(_l) != 0 else None
            else:
                _l = list(['{}\t{}'.format(s, 'valid fb2 tag'), '{}>'.format(s)]\
                          for s in \
                          filter(lambda s: s.startswith(prefix), valid_fb2_tags)
                         )
                return _l if len(_l) != 0 else None
        return None

