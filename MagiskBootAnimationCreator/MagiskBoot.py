from genericpath import isdir, isfile
from os import getcwd, listdir, mkdir, remove
import os
from shutil import copyfile, move, rmtree
import sys
import zipfile
from PyQt5 import QtWidgets,uic
from PIL import Image
# ui class
class UI():
    # varible
    app = None
    window = None
    selectedfile = None
    #
    # animation type
    # 0 = mp4
    # 1 = folder
    # 2 = gif
    anitype = None
    # startup
    def init():
          global app,window
          QtWidgets.QApplication.quit()
          app = QtWidgets.QApplication(sys.argv)
          window = UI.mainwindow()
          app.exec_()
    # main window
    class mainwindow(QtWidgets.QMainWindow):

        def __init__(self):
        
            type = QtWidgets.QPushButton
            super(UI.mainwindow,self).__init__()
            uic.loadUi(getcwd()+"/pages/main.ui",self)

            self.button = self.findChild(type,'mp4select')
            self.button.clicked.connect(self.selectfilemp4)
            self.button2 = self.findChild(type,'pngselect')
            self.button2.clicked.connect(self.selectfilepng)
            self.button3 = self.findChild(type,"gifselect")
            self.button3.clicked.connect(self.selectfilegif)
            self.show()

        def selectfilemp4(self):
            global window,selectedfile,anitype
            selectedfile = QtWidgets.QFileDialog.getOpenFileName(filter="mp4 files (*.mp4)")
            print("mp4: "+  str(selectedfile) )  
            if  selectedfile[0]:
                anitype = 0
                window = UI.editor()
                window.show()
                window.activateWindow()

        def selectfilepng(self):
            global window,selectedfile,anitype
            selectedfile = QtWidgets.QFileDialog.getExistingDirectory()
            print("directory: " + selectedfile)
            if  selectedfile:
                anitype = 1
                window = UI.editor()
                window.show()
                window.activateWindow()
        
        def selectfilegif(self):
            global window,selectedfile,anitype
            selectedfile = QtWidgets.QFileDialog.getOpenFileName(filter="gif files (*.gif)")
            print("gif: "+  str(selectedfile) )  
            if  selectedfile[0]:
                anitype = 2
                window = UI.editor()
                window.show()
                window.activateWindow()

    class editor(QtWidgets.QMainWindow):

        def __init__(self):
            type = QtWidgets.QSpinBox
            type1 = QtWidgets.QPushButton
            type2 = QtWidgets.QComboBox
            super(UI.editor,self).__init__()
            uic.loadUi(getcwd()+"/pages/editor.ui",self)
            self.width = self.findChild(type,"device_width")
            self.height = self.findChild(type,"device_height")
            self.fps = self.findChild(type,"fps")
            self.play_count = self.findChild(type,"play_count")
            self.move_on = self.findChild(type1,"move_on")
            self.play_type = self.findChild(type2,"play_type")
            self.boot_end_pause = self.findChild(type,"boot_end_pause")
            self.move_on.clicked.connect(self.is_done)
        def error(self,t):
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle("oops")
            if t == 1:
                message_box.setText("select something from play type")
            else:
                message_box.setText("values should not be 0")
            message_box.exec_()
        def create_gif_boot(self,at):
            # create part 0
            target_dir = getcwd()+"/bootanizip/"
            type = None
            if self.play_type.currentIndex() == 1:
                type = "p"
            elif self.play_type.currentIndex() == 2:
                type = "c"
            # check if folder
            if not isdir(target_dir):
                mkdir(target_dir)
            #check if tmp files exist
            
            if isdir(target_dir+"part0"):
                rmtree(target_dir+"part0",ignore_errors=True)
               
            if isfile(target_dir+"desc.txt"):
                remove(target_dir+"desc.txt")
            if isfile(target_dir+"bootanimation.zip"):
                remove(target_dir+"bootanimation.zip")
            mkdir(target_dir+"part0")

            f = open(target_dir+"desc.txt","w")
            f.write(str(
                self.width.value())
                +" "
                +str(self.height.value())
                +" "+
                str(self.fps.value())
                # break
                +"\n"+
                # play type
                type
                +" "+
                str(self.play_count.value())
                +" "+
                str(self.boot_end_pause.value())
                +" "+
                "part0"
                +"\n "
                )
            f.close()
            # now check the type
            if at == 1:
                # that's a folder
                for file in listdir(selectedfile):
                   copyfile(selectedfile+"/"+file,target_dir+"part0/"+file)

            #
            if at == 2: 
                count = 0
                # that's a gif
                # open the gif and split them into images
                gifobj = Image.open(selectedfile[0])
            
                for i in range(0,gifobj.n_frames):
                    # get all frames and save to folde
                    gifobj.seek(i)
                    gifobj.save(target_dir+"part0/"+str("{:05d}".format(count+1))+".png","PNG")
                   # frame.save(
                    count +=1
                gifobj.close()
            # zip the folder
            
            zf = zipfile.ZipFile(target_dir+'bootanimation.zip','w',compression=zipfile.ZIP_STORED)
            zf.write(target_dir+"desc.txt","desc.txt")
            for file in listdir(target_dir+"part0"):
                zf.write(target_dir+"part0/"+file,"part0/"+file)
            zf.close()

        def create_video_boot():
            None
        def is_done(self):
           
            global anitype
            dns = False
            # check if the values are above 1
            if self.width.value() == 0:
                dns = True
            if self.height.value() == 0:
                dns = True
            if self.fps.value() == 0:
                dns = True
            if self.play_type.currentText() == "select":
               self.error(1)
            if dns:
               self.error(None)
            else:
               if anitype == 1 or anitype == 2:
                  self.create_gif_boot(anitype)
            # is an mp4 

            # when done open last folder
            global window
            window = UI.sig()
            window.show()
            window.activateWindow()
    class sig(QtWidgets.QMainWindow):
        def __init__(self):
            type = QtWidgets.QTextEdit
            type1 = QtWidgets.QPushButton
            super(UI.sig,self).__init__()
            uic.loadUi(getcwd()+"/pages/2.ui",self)
            self.button = self.findChild(type1,"finaldone")
            self.magisk_id = self.findChild(type,"magisk_id_e")
            self.name = self.findChild(type,"name_e")
            self.author = self.findChild(type,"author_e")
            self.description = self.findChild(type,"description_e")
            self.button.clicked.connect(self.compile_everything)
        def zipdir(self,folder_path,zip):
            len_dir_path = len(folder_path)
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip.write(file_path, file_path[len_dir_path:])
        def error(self):
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle("oops")
            message_box.setText("enter something")   
            message_box.exec_()     
        def compile_everything(self):
            dns = False
            if self.magisk_id.toPlainText() == "":
                dns = True
            if self.name.toPlainText() == "":
                dns = True
            if self.author.toPlainText() == "":
                dns = True
            if self.description.toPlainText() == "":
                dns = True

            if dns:
                self.error()
            else:
                zip_target = getcwd()+"/"
                target_dir = getcwd()+"/flashzip/"
                target_dir2 = getcwd()+"/bootanizip/"
                # write to magisk module.prop
                if isfile(target_dir+"module.prop"):
                    # remove that
                    remove(target_dir+"module.prop")
                
                f = open(target_dir+"module.prop","w")
                f.write(
                    "id=" + self.magisk_id.toPlainText() + "\n"
                    "name=" + self.name.toPlainText() + "\n"
                    "version=v1" + "\n"
                    "versionCode=1" + "\n"
                    "author=" + self.author.toPlainText() +  "\n"
                    "description=" + self.description.toPlainText() + "\n"
                    "minMagisk=19000" 
                )
                f.close()
                # move that zip file to the folder
                move(target_dir2+"bootanimation.zip",target_dir+"system/product/media/"+"bootanimation.zip")
                # zip everything
                z = zipfile.ZipFile(zip_target+self.name.toPlainText()+'.zip','w',compression=zipfile.ZIP_STORED)
                self.zipdir(target_dir,z)
                z.close()
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("info")
                message_box.setText("flashable magisk zip saved at "+zip_target+" as "+self.name.toPlainText()+'.zip')   
                message_box.exec_()    
                # go back
                global window
                window = UI.mainwindow()
                window.show()
                window.activateWindow()
                
UI.init()
