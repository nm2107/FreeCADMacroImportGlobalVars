from os import path
import FreeCAD


class FCProject():
    """Contains the values defined in the FCProject file"""
    def __init__(self, filePath: str, values: dict):
        """
        filepath : the path of the FCProject file
        values : the parsed values (key-val dict)
        """
        self.filePath = filePath
        self.globalVarsFilePath = values.get('GLOBAL_VARS_FILE_PATH')
        self.globalVarsSpreadsheetName = values.get('GLOBAL_VARS_SPREADSHEET_NAME')


    def getFilePath(self) -> str:
        return self.filePath


    def getGlobalVarsFilePath(self) -> str:
        return self.globalVarsFilePath


    def getGlobalVarsSpreadsheetName(self) -> str:
        return self.globalVarsSpreadsheetName


def readFcProjectFile(filepath: str) -> FCProject:
    defaultValues: dict = {
        'GLOBAL_VARS_FILE_PATH': path.join(path.dirname(filepath), 'GlobalVars.FCStd'),
        'GLOBAL_VARS_SPREADSHEET_NAME': 'GlobalVars',
    }
    parsedValues: dict = {}

    file = open(filepath, 'r')
    for line in file:
        split = line.strip().split('=')

        if len(split) < 2:
            continue

        key = split[0]

        if key not in defaultValues:
            continue

        val = split[1]

        parsedValues[key] = val

    file.close()

    return FCProject(filepath, defaultValues | parsedValues)


def fetchFcProject(childPath: str) -> FCProject:
    """Recursively looks up for a FCProject file in the current path and ancestors.
    When found, returns a FCProject object containing the file data.
    """

    (parentPath, childElement) = path.split(childPath)

    if ('' == childElement):
        raise FileNotFoundError('FCProject file not found')

    fcprojectFilePath = path.join(parentPath, 'FCProject')

    if not path.isfile(fcprojectFilePath):
        return fetchFcProject(parentPath)

    return readFcProjectFile(fcprojectFilePath)


def documentHasALinkToGlobalVars(document: FreeCAD.Document, globalVarsFileAbsolutePath: str, globalVarsSpreadsheetName: str) -> bool:
    for obj in document.Objects:
        if 'App::Link' != obj.TypeId:
            continue

        if 'Spreadsheet::Sheet' != obj.LinkedObject.TypeId:
            continue

        if globalVarsFileAbsolutePath != obj.LinkedObject.Document.FileName:
            continue

        if globalVarsSpreadsheetName != obj.LinkedObject.Label:
            continue

        return True

    return False


def makeGlobalVarsLink(document: FreeCAD.Document, globalVarsFileAbsolutePath: str, globalVarsSpreadsheetName: str) -> None:
    globalVarsDocument = FreeCAD.openDocument(globalVarsFileAbsolutePath)
    FreeCAD.setActiveDocument(document.Name)

    spreadsheetObject: FreeCAD.DocumentObject = None

    for obj in globalVarsDocument.Objects:
        if 'Spreadsheet::Sheet' != obj.TypeId:
            continue

        if globalVarsSpreadsheetName != obj.Label:
            continue

        spreadsheetObject = obj
        break

    if not spreadsheetObject:
        raise NameError('GlobalVars document "' + globalVarsFileAbsolutePath + '" doesn\'t have a "' + globalVarsSpreadsheetName + '" spreadsheet.')

    link = document.addObject('App::Link', globalVarsSpreadsheetName)
    link.LinkedObject = spreadsheetObject


def linkGlobalVarsToDocument(document: FreeCAD.Document) -> None:
    documentPath: str = document.FileName
    fcproject: FCProject = None

    try:
        fcproject = fetchFcProject(documentPath)
    except FileNotFoundError as e:
        FreeCAD.Console.PrintLog(e)
        return

    globalVarsFileAbsolutePath = path.normpath(path.join(path.dirname(fcproject.getFilePath()), fcproject.getGlobalVarsFilePath()))

    if not path.isfile(globalVarsFileAbsolutePath):
        FreeCAD.Console.PrintWarning('GlobalVars file "' + globalVarsFileAbsolutePath + '" does not exist.')
        return

    if documentPath == globalVarsFileAbsolutePath:
        # do not link GlobalVars to itself
        return

    if documentHasALinkToGlobalVars(document, globalVarsFileAbsolutePath, fcproject.getGlobalVarsSpreadsheetName()):
        # already linked
        return

    try:
        makeGlobalVarsLink(document, globalVarsFileAbsolutePath, fcproject.getGlobalVarsSpreadsheetName())
    except NameError as e:
        FreeCAD.Console.PrintError(e)
        return

    document.recompute()
