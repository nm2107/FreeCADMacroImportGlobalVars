import FreeCAD
from ImportGlobalVars import linkGlobalVarsToDocument


class ImportGlobalVarsDocumentObserver():
    def slotStartSaveDocument(self, document: FreeCAD.Document, docName: str) -> None:
        linkGlobalVarsToDocument(document)


def registerObserver() -> None:
    observer = ImportGlobalVarsDocumentObserver()
    FreeCAD.addDocumentObserver(observer)
