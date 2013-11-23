HNReader for Mac OS X
=====================
Qt PySide based python application to read ycombinator hacker news web page.
Depends mainly on 
- Pyside: http://qt-project.org/wiki/PySide (available through brew on Mac OS X)
- mako template engine
- lxml

Run in a terminal with 'python hnreader.py'

To create a self contained python app bundle: use py2app
`pip install py2app`
then run inside the project directory
`python setup.py py2app`

Fork and contribute!
