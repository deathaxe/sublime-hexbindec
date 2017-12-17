import re

import sublime
import sublime_plugin

# ============================================================================
# CONFIGURATION DESCRIPTION
#
# Each TextCommand uses the view.settings() object to look for custom format
# patterns. That's why it is possible to define a hex/bin for each type of
# source with the help of language specific settings files.
#
# If no setting is found the following patterns are used by default to extract
# the hex/bin value from the selected text and format the output of the
# converted value.
#
# REMARKS
#     A hex/bin value can be single quoted.
#
# EXAMPLE CONFIGURATION
#
#    // Binaries look like 'B101110'
#    "convert_src_bin": "'B([01]+)'",
#    // After convertion to binary format the output as follows
#    "convert_dst_bin": "'B{0:b}'",
#
#    // Hexadecimals look like 'H1AF23'
#    "convert_src_hex": "'H([0-9A-Z]+)'",
#    // After convertion to hexadecimal format the output as follows
#    "convert_dst_hex": "'H{0:X}'",
#
#    // Exponential decimals look like 1.42EX-5
#    "convert_src_exp": "\\b([1-9]\\.\\d+)EX([-+]?\\d+)\\b",
#    "convert_dst_exp": "EX",
# ============================================================================
# Default binary destination format
_CONVERT_DST_BIN_DFLT = '{0:b}'
# Default hexadecimal destination format
_CONVERT_DST_HEX_DFLT = '{0:#x}'
# Default exponential destination format
_CONVERT_DST_EXP_DFLT = r'e'
# Default binary search pattern
_CONVERT_SRC_BIN_DFLT = r'\b(?:0b)?([01]+)\b'
# Default hexadecimal search pattern
_CONVERT_SRC_HEX_DFLT = r'\b(?:0x)?([0-9a-f]+)h?\b'
# Default exponential search pattern
_CONVERT_SRC_EXP_DFLT = r'\b(\d+\.\d+)e([-+]?\d+)\b'
# ============================================================================


def load_pattern(view, name, default):
    try:
        return re.compile(view.settings().get(name, default))
    except:
        return re.compile(default)


class BinToDecCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        r = load_pattern(view, 'convert_src_bin', _CONVERT_SRC_BIN_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    # if source is single quoted, expand selection
                    # by one more character before and after the word.
                    if r.pattern[0] == '\'':
                        sel.a -= 1
                        sel.b += 1

                match = r.match(view.substr(sel))
                view.replace(edit, sel, str(int(match.group(1), 2)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid binary value(s)!" % num_skip)


class BinToHexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_format = view.settings().get('convert_dst_hex', _CONVERT_DST_HEX_DFLT)
        r = load_pattern(view, 'convert_src_bin', _CONVERT_SRC_BIN_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    # if source is single quoted, expand selection
                    # by one more character before and after the word.
                    if r.pattern[0] == '\'':
                        sel.a -= 1
                        sel.b += 1

                match = r.match(view.substr(sel))
                view.replace(edit, sel, dst_format.format(int(match.group(1), 2)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid binary value(s)!" % num_skip)


class DecToBinCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_format = view.settings().get('convert_dst_bin', _CONVERT_DST_BIN_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)

                dec = view.substr(sel).strip()
                view.replace(edit, sel, dst_format.format(int(dec)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid decimal value(s)!" % num_skip)


class DecToHexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_format = view.settings().get('convert_dst_hex', _CONVERT_DST_HEX_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)

                dec = int(view.substr(sel).strip())
                view.replace(edit, sel, dst_format.format(dec))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid decimal value(s)!" % num_skip)


class HexToBinCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_format = view.settings().get('convert_dst_bin', _CONVERT_DST_BIN_DFLT)
        r = load_pattern(view, 'convert_src_hex', _CONVERT_SRC_HEX_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    # if source is single quoted, expand selection
                    # by one more character before and after the word.
                    if r.pattern[0] == '\'':
                        sel.a -= 1
                        sel.b += 1

                # valid hex: 10 , 0x10 , 0x10h , 10h, h10
                match = r.match(view.substr(sel))
                view.replace(edit, sel, dst_format.format(int(match.group(1), 16)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid hexadecimal value(s)!" % num_skip)


class HexToDecCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        r = load_pattern(view, 'convert_src_hex', _CONVERT_SRC_HEX_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    # if source is single quoted, expand selection
                    # by one more character before and after the word.
                    if r.pattern[0] == '\'':
                        sel.a -= 1
                        sel.b += 1

                # validate selection
                match = r.match(view.substr(sel))
                # replace selection with the result
                view.replace(edit, sel, str(int(match.group(1), 16)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid hexadecimal value(s)!" % num_skip)


class ExpToDecCommand(sublime_plugin.TextCommand):
    """
    Convert real values with exponent to normal decimal.

    Minimum: 9.0e-4
    Maximum: 9.0e15

    EXAMPLE:
        1.42e3  ->  1420
    """

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        r = load_pattern(view, 'convert_src_exp', _CONVERT_SRC_EXP_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    while view.substr(sel.a - 1) in "0123456789.eExX-":
                        sel.a -= 1
                    while view.substr(sel.b) in "0123456789.eExX-":
                        sel.b += 1

                # validate selection
                match = r.match(view.substr(sel))
                # convert the match and round by 18 digits after comma
                result = round(float(match.group(1)) * 10 ** float(match.group(2)), 18)
                # replace selection with the formated result
                view.replace(edit, sel, str(result).rstrip('0').rstrip('.'))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid exponential value(s)!" % num_skip)


class DecToExpCommand(sublime_plugin.TextCommand):
    """
    Convert a real value to exponential format.

    Minimum: 9.0e-4
    Maximum: 9.0e15

    EXAMPLE:
        1420  ->  1.42e3
    """

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_pattern = view.settings().get('convert_dst_exp', _CONVERT_DST_EXP_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    while view.substr(sel.a - 1) in "0123456789.":
                        sel.a -= 1
                    while view.substr(sel.b) in "0123456789.":
                        sel.b += 1

                # convert the value
                base = float(view.substr(sel))
                exp = 0
                while base > 10:
                    base /= 10
                    exp += 1
                while base < 1:
                    base *= 10
                    exp -= 1

                # convert base to string
                base = str(base).rstrip('0').rstrip('.')
                # replace selection with the formated result
                view.replace(edit, sel, base + dst_pattern + str(exp))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid decimal value(s)!" % num_skip)
