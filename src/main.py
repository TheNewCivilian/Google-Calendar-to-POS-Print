from escpos.printer import Usb
from subprocess import Popen, PIPE

# }
p = Popen(["gcalcli", "agenda","0:00am", "11:59pm","--nocolor"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate()
#print output

print output
taskbuffer = output.split(" ")
taskbuffer[:] = [item for item in taskbuffer if item != '']

title = ""
entry = ""
dayly_entry = ""
entry_list = []
dayly_entry_list = []
dayly = True
for item in taskbuffer:
    if taskbuffer.index(item) < 3:
        #print "->" + item
        #Printer.text(item + " ")
        title += str(item + " ")
        print title
    else:
        if ':' not in item and dayly is True:
            if '\n' not in item:
                dayly_entry += str(item + " ")
            else:
                dayly_entry += str(item)
                dayly_entry = dayly_entry.replace('\n','')
                dayly_entry_list.append(dayly_entry)
                dayly_entry = ""
                print dayly_entry_list
        else:
            dayly = False
            if '\n' and ':' not in item:
                entry += str(item + " ")
            else:
                if len(entry) > 0:
                    entry = entry.replace('\n','')
                    entry_list.append(entry)
                entry_list.append(item)
                entry = ""
                print entry_list
Printer = Usb(0x0416,0x5011)
Printer.set(align=u'center', font=u'a', width=2, height=2, density=9, invert=False, smooth=True, flip=False)
Printer.text(title+"\n")
Printer.set(align=u'center', font=u'a', width=1, height=1, density=9, invert=False, smooth=True, flip=False)
Printer.text("\n------- Heute -------\n\n")
Printer.set(align=u'right', font=u'a', width=1, height=1, density=9, invert=False, smooth=True, flip=False)
for item in dayly_entry_list:
    Printer.text('{:3s}  {:>27s}'.format( "[ ]", item) + "\n\n")
Printer.set(align=u'center', font=u'a', width=1, height=1, density=9, invert=False, smooth=True, flip=False)
Printer.text("\n------- Tasks -------\n\n")
Printer.set(align=u'right', font=u'a', width=1, height=1, density=9, invert=False, smooth=True, flip=False)
for item in entry_list:
    if entry_list.index(item)%2 == 0 and entry_list.index(item)+2 <len(entry_list):
        Printer.text('{:3s} {:>5s} {:>23s}'.format('[ ]', item, entry_list[entry_list.index(item)+1]) + "\n")
Printer.cut()
