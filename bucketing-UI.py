from tkinter import *
import os
import copy
from PIL import Image, ImageTk
from tkinter import filedialog

root = Tk()
root.title('EveryDream Bucket Checker')
root.geometry("1280x720+100+100")
#root.iconbitmap("bucket.ico")

frame = LabelFrame(root)
frame.pack(fill=BOTH, padx=5, pady=5)

def setDirectory():
  root.directory = filedialog.askdirectory()
  directory.delete(0, END)
  directory.insert(0, root.directory)

#fileIcon = PhotoImage(file="open_folder.png")
#button = Button(frame, image = fileIcon, command=setDirectory)
button = Button(frame, text="File", command=setDirectory)
button.grid(row=0, column= 0, padx=5, pady=5)

directory = Entry(frame, width=50)
directory.grid(row=0, column=1, padx=(3,15))

batchLabel = Label(frame, text="Batch: ")
batchLabel.grid(row=0, column=2, padx=(7,0))

batch = Entry(frame, width=3)
batch.insert(0, "1")
batch.grid(row=0, column=3, padx=(1,10))

errorLabel = Label(frame, text="")
errorLabel.grid(row=0, column=10, padx=(7,5))

bucketValues = [
[256, 832, 0, []],
[320, 768, 0, []],
[384, 640, 0, []],
[448, 576, 0, []],
[512, 512, 0, []],
[576, 448, 0, []],
[640, 384, 0, []],
[768, 320, 0, []],
[832, 256, 0, []],
[896, 256, 0, []],
[960, 256, 0, []],
[1024, 256, 0, []],
]

imgs = []
frames = []
labels = []
widgetList = []
height = 20

def printValues():
  
  error = 0
  # worst error handling you'll ever see
  if not os.path.exists(directory.get()):
    error = 1

  batchNum = batch.get()
  if not batchNum.isnumeric():
    error += 2
  
  batchNum = int(batchNum)
  if batchNum <= 0:
    error += 2

  if error == 3:
    errorLabel.config(text="Unknown directory and incorrect batch number")
    return
  elif error == 1:
    errorLabel.config(text="Unknown directory")
    return
  elif error == 2:
    errorLabel.config(text="Batch number must be a numeric value greater than 0")
    return

  error = 0
  errorLabel.config(text="")
  numOfImages = 0
  
  # restart and clear old values
  for frame in frames:
    frame.destroy()

  for widget in widgetList:
    widget.destroy()
  
  imgs.clear()
  frames.clear()
  labels.clear()

  buckets = copy.deepcopy(bucketValues)
  #####

  ## calculate buckets
  for filename in os.listdir(root.directory):
    f = directory.get() + '\\' + filename
    if os.path.isfile(f) and f.lower().endswith(('.png', '.jpg', '.jpeg')):
      numOfImages += 1
      img = Image.open(f)
      ratio = img.width/img.height
      addBucket = min(range(len(buckets)), key=lambda i: abs((buckets[i][0]/buckets[i][1])-ratio))
      buckets[addBucket][2] = buckets[addBucket][2] + 1
      buckets[addBucket][3].append(filename)

  #display to UI
  frame2 = Frame(root)
  frame2.pack(fill=BOTH, padx=5, pady=5, expand = 1)
  widgetList.append(frame2)

  canvas = Canvas(frame2)
  canvas.pack(side=LEFT, fill=BOTH, expand=1)
  widgetList.append(canvas)

  scroll = Scrollbar(frame2, orient=VERTICAL)
  scroll.pack(side=RIGHT, fill=Y)
  scroll.config(command=canvas.yview)
  widgetList.append(scroll)

  canvas.configure(yscrollcommand=scroll.set)
  canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

  f2 = Frame(canvas)
  widgetList.append(f2)
  canvas.create_window((0,0), window=f2, anchor=NW)

  for element in buckets: 

    i = 0
    j = 0
    totalWidth = 0

    height = 100
    if clicked.get() == "Small":
      height = 50
    elif clicked.get() == "Medium":
      height = 100
    elif clicked.get() == "Large":
      height = 150

    if element[2] != 0:
      dropout = element[2]%int(batchNum)
      print("[", element[0], ", ", element[1], "]  ", element[2], " | ", dropout, "dropped")
      tempFrame = LabelFrame(f2, text= "[" + str(element[0]) + ", " + str(element[1]) + "]   " + str(dropout) + " dropped")
      tempFrame.pack(fill=BOTH, padx=5, pady=5, expand=1)
      frames.append(tempFrame)

      for img in element[3]:
        print(img)
        
        image = Image.open(root.directory + '\\' + img)
        
        ratio = image.width/image.height
        newW = round(height * ratio)
        image.width
        resize = image.resize((newW,height))
        totalWidth += resize.width + 5

        imgs.append(ImageTk.PhotoImage(resize))
        if totalWidth + resize.width >= root.winfo_width() - 30:
          totalWidth = 0
          j += 1
          i = 0
        tempLabel = Label(tempFrame, image=imgs[-1]).grid(row= j, column=i, padx=5, pady=5)
        labels.append(tempLabel)
        i += 1
      print("-------------------------------------------- \n")
        
      


  

startButton = Button(frame, text = "START", command=printValues, width=6)
startButton.grid(row=0, column=4)

clicked = StringVar()
clicked.set("Medium")
dropDown = OptionMenu(frame, clicked, "Small", "Medium", "Large")
dropDown.config(width=8)
dropDown.grid(row=0, column=5, padx=(7,5))

root.mainloop()