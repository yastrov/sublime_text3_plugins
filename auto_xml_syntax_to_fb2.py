import sublime
import sublime_plugin
# For document for API see:
# https://www.sublimetext.com/docs/3/api_reference.html#sublime.View
# Also you can do it next way:
# Open file, set syntax style manually and next with menu:
# View -> Syntax -> Open all with current extension with...

class AutoXMLSyntaxForFB2(sublime_plugin.EventListener):
    def on_load(self, view):
        fname = view.file_name()
        if fname and fname.endswith('.fb2'):
            syntax_file = 'Packages/XML/XML.tmLanguage'
            # No way to get it right way. Next code doesn't work.
            #syntax_file = view.settings().get('XML')
            view.assign_syntax(syntax_file)
