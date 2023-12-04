# FreeCAD Mod Import global vars

A FreeCAD mod to automatically import (make a link to) a spreadsheet
containing the vars to be used for the whole project.
The spreadsheet location is defined in a `FCProject` file at the root of your
project dir.

**Installation :**

Clone this repo in the `Mod` directory of your FreeCAD
[root directory](https://wiki.freecad.org/Installing_more_workbenches).


**How to use :**

- Create a .FCStd file containing a spreadsheet to define your global vars for
your project.
- Create the `FCProject` file which tells where to find the spreadsheet, e.g. :

```
GLOBAL_VARS_FILE_PATH=GlobalVars.FCStd
GLOBAL_VARS_SPREADSHEET_NAME=GlobalVars
```

- Create a new .FCStd file in your project and save it.
- Result : the newly created file now has a link to the global vars
spreadsheet.

**What it does :**

When saving a .FCStd document, the mod looks up for the `FCProject` file
and parses it to retrieve the location of your defined global vars file
and spreadsheet name.
Then, it opens the global vars file and makes a link to its spreadsheet into
the currently active document.

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

When creating ans saving a new document e.g. `./model/parts/Fork.FCStd`, the
`GlobalVars` spreadsheet is automatically imported into this document.

**Why ?**

In order to avoid to manually import (i.e. make a link to) a spreadsheet
from an other document into the active one.
It will speed up the FreeCAD workflow.
