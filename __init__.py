# -*- coding: utf-8 -*-

"""gopass search.

Synopsis: <trigger> <filter>"""


from albert import *
import subprocess
import os
from shutil import which


__title__ = "gopass search"
__prettyname__ = 'gopass'
__version__ = "0.1.0"
__triggers__ = "gp "
__authors__ = "Chad Jones"
__py_deps__ = ["shutil"]
__exec_deps__ = ['gopass']

if not which('gopass'):
    raise Exception("`gopass` is not in $PATH.")\

ICON_PATH = os.path.dirname(__file__)+"/gopass.png"

def handleQuery(query):
    """
    Handle query
     :param str query: Query
     :return list
    """
    if not query.isTriggered:
        return None

    stripped = query.string.strip()

    if stripped:
        try:
            gopass = subprocess.Popen(['gopass', 'ls', '-f'], stdout=subprocess.PIPE, encoding='utf8')
            try:
                output = subprocess.check_output(['grep', '-i', stripped], stdin=gopass.stdout, encoding='utf8')
            except subprocess.CalledProcessError as e:
                return Item(
                    id=__prettyname__,
                    icon=ICON_PATH,
                    text=__prettyname__,
                    subtext=f'No results found for {stripped}',
                    completion=query.rawString
                )
            items = []
            for line in output.splitlines():
                items.append(Item(
                    id=__prettyname__,
                    icon=ICON_PATH,
                    text=line.split('/')[-1],
                    subtext='/'.join(line.split('/')[:-1]),
                    completion=query.rawString,
                    actions=[
                        ProcAction("Copy password to clipboard", ["gopass", "-c", line]),
                        ClipAction(
                            text=f"Copy username to clipboard",
                            clipboardText=line.split('/')[-1])
                    ]
                ))

            return items

        except subprocess.CalledProcessError as e:
            return Item(
                id=__prettyname__,
                icon=ICON_PATH,
                text=f'Error: {str(e.output)}',
                subtext=str(e),
                completion=query.rawString,
                actions=[ClipAction('Copy CalledProcessError to clipboard', str(e))]
            )
        except Exception as e:
            return Item(
                id=__prettyname__,
                icon=ICON_PATH,
                text=f'Generic Exception: {str(e)}',
                subtext=str(e),
                completion=query.rawString,
                actions=[ClipAction('Copy Exception to clipboard', str(e))]
            )
    
    else:
        return Item(
            id=__prettyname__,
            icon=ICON_PATH,
            text=__prettyname__,
            subtext='Search gopass',
            completion=query.rawString,
        )