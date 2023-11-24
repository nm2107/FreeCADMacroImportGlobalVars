# FreeCAD Macro Import global vars

A FreeCAD macro to import (make a link to) a spreadsheet containing vars to be
used for the whole project. The spreadsheet location is defined in a `FCProject`
file at the root of your project dir.

**How to use :**

- Create a .FCStd file containing a spreadsheet to define your global vars for
your project.
- Create the `FCProject` file which tells where to find the spreadsheet, e.g. :

```
GLOBAL_VARS_FILE_PATH=GlobalVars.FCStd
GLOBAL_VARS_SPREADSHEET_NAME=GlobalVars
```

- Create a new .FCStd file in your project and save it.
- Invoke the macro : the newly created file now has a link to the global
vars spreadsheet.

**What it does :**

It looks up for the `FCProject` file and parses it to retrieve the location of
your defined global vars file and spreadsheet name. Then, it opens the global
vars file and makes a link to its spreadsheet into the currently active
document.

Exemple of a project structure : 

```
MyProject/
├── FCProject
├── model/
│   ├── GlobalVars.FCStd
│   └── parts/
│       └── Plate.FCStd
├── README.md
```

In this exemple, the `FCProject` file content would be :

```
GLOBAL_VARS_FILE_PATH=./model/GlobalVars.FCStd
GLOBAL_VARS_SPREADSHEET_NAME=GlobalVars
```

The use of the macro when the `model/parts/Plate.FCStd` document is opened would
import the `GlobalVars` spreadsheet into this document.

**Why ?**

In order to avoid to manually import (i.e. make a link to) a spreadsheet
from an other document into the active one.
It will speed up the FreeCAD workflow.

**Improvements**

It would be nice to automatically invoke this macro when the document is saved,
so global vars would be automatically exposed. FreeCAD's document observers
might be helpful for that.
