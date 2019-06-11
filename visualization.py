
'''
    Comp 380 group project
    Group members: Gigi Lucena, Glenda Gonzalez, Daniel Stein,
                   Jonathan Slauter, Andre Tecson
    Date created: 06/22/2018
    Created by: Daniel Stein
    Data Modified: 07/02/2018
    Modified by:  Gigi Lucena
    Description: Visualization
'''

import Tkinter as tk
import ttk
import multiprocessing
import socket
import tkMessageBox
import os

import camera
import config


'''
    global variables
'''
ips = []
listOfProcesses =[]
fileName = 'settings.json'

configuration = config.config(fileName)
settings = configuration.loadFile()


'''
    Defining buttons actions
'''

def enter_ip():
    global ips
    global listOfProcesses
    global win
    global listbox

    action.configure()  # name is the string of the IP webcam url to be parsed

    try:
        ip = name.get()
        socket.inet_aton(ip)
        url = 'http://' + ip + ':8080/video'  # 'http://172.28.136.139:8080/video'

        cam = camera.Camera(url)
        ips.append({"ip": ip, "description": "camera " + ip})

        listbox.insert('end',"camera " + ip )

        # start a process to each camera ip entered
        process = multiprocessing.Process(target=cam.start)
        listOfProcesses.append(process) # append the process to a list
        process.start()

        name_entered.delete(0, 'end') #clear text from entry field
    except socket.error:
        tkMessageBox.showinfo(title="Multi Camera", message="Invalid IP! Please, enter a valid IP. ")


def save_configuration():
    # save active camera windows to JSON file
    global ips
    configuration.saveFile(ips)
    tkMessageBox.showinfo(title="Multi Camera", message="Preferences saved! ")


def exit_application():

    for process in listOfProcesses: # terminate all processes
        process.terminate()

    win.quit()
    win.destroy()
    exit()

def loadCameras():
    global settings
    global listbox

    for ip in settings["ips"]:
        print('Loading...')

        url = 'http://' + ip["ip"] + ':8080/video'  # 'http://172.28.136.139:8080/video'
        cam = camera.Camera(url)
        ips.append({"ip": ip["ip"], "description": "camera " + ip["ip"]})
        listbox.insert('end',"camera " + ip["ip"] )

        # start a process to each camera ip entered
        process = multiprocessing.Process(target=cam.start)
        listOfProcesses.append(process) # append the process to a list
        process.start()



'''
   create and start GUI
'''
# Create instance
win = tk.Tk()

# Add a title
win.title("Multicam")
win.resizable(0, 0)

# Adding a label
mighty = ttk.LabelFrame(text='Enter Camera IP')
mighty.grid(column=0, row=0, padx=12, pady=18)

# Adding a Textbox Entry widget
name = tk.StringVar()
name_entered = ttk.Entry(mighty, width=12, textvariable=name)
name_entered.bind("<Return>", (lambda event: enter_ip()))
name_entered.grid(column=0, row=1, sticky='W')  # align left/West
name_entered.config(width=27)

# Adding buttons to gui
action = ttk.Button(mighty, text="+", command=enter_ip)
action.grid(column=1, row=1, padx=8)


# Adding a label
labelButton = ttk.Frame()
labelButton.grid(column=0, row=4, padx=12, pady=18)

btnSaveConfiguration = ttk.Button(labelButton, text="Save", command=save_configuration)
btnSaveConfiguration.grid(column=0, row=4)

btnExit = ttk.Button(labelButton, text='Exit', command=exit_application)
btnExit.grid(column=1, row=4,)

name_entered.focus()  # Place cursor into name Entry

listbox = tk.Listbox(mighty)
listbox.grid(column=0, row=2)
listbox.config(width=27)

listbox.insert('end', "List of cameras IP")
listbox.itemconfig(0,{'bg':'blanchedalmond'})

# if exists a file settings load the cameras in that file
if os.path.exists(fileName):
    print('found')
    loadCameras()


win.mainloop()
