from rooter.table import Table
from rooter import print, rooter

t = Table()
t.addColumn("test")
t.addRow(['test'])
t.addRow(["content"])
print(t)