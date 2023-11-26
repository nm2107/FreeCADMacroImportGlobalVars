# @see https://wiki.freecad.org/Macro_at_Startup

import FreeCADGui


def registerGlobalVarsImportDocumentObserver(wbName: str) -> None:
    # Do not run when NoneWorkbench is activated because UI
    # isn't yet completely there
    if 'NoneWorkbench' == wbName:
        return

    # Unregister this startup handler to make sure that
    # the document observer is only added once.
    FreeCADGui.getMainWindow().workbenchActivated.disconnect(registerGlobalVarsImportDocumentObserver)

    from ImportGlobalVarsDocumentObserver import registerObserver
    registerObserver()

# The following 2 lines are important because InitGui.py files are passed
# to the exec() function and the function to bind wouldn't be visible outside.
# So explicitly bind it to __main__
import __main__
__main__.registerGlobalVarsImportDocumentObserver = registerGlobalVarsImportDocumentObserver

# Register the function to FC startup
FreeCADGui.getMainWindow().workbenchActivated.connect(registerGlobalVarsImportDocumentObserver)
