from tkinter import *
import customtkinter as ct
import functools
from sys import platform
from datetime import datetime
import Operations as OP

fp = functools.partial

class VerticalScrolledFrame(ct.CTkFrame):
    """
    A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    * This comes from a different naming of the the scrollwheel 'button', on different systems.
    """
    def __init__(self, parent, *args, **kw):

        super().__init__(parent, *args, **kw)

        
        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = ct.CTkScrollbar(self, orientation=VERTICAL)
        self.vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)

        self.canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self.vscrollbar.set,bg="black")

        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.vscrollbar.configure(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = ct.CTkFrame(self.canvas,fg_color=None)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior,
                                           anchor=NW)

        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.canvas.bind('<Enter>', self._bind_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbind_from_mousewheel)
        
        
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar



    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)

        if self.interior.winfo_reqwidth() != self.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=self.winfo_width())

    # This can now handle either windows or linux platforms
    def _on_mousewheel(self, event, scroll=None):

        if platform == "linux" or platform == "linux2":
            self.canvas.yview_scroll(int(scroll), "units")
        else:
            self.canvas.yview_scroll(int(-1*((event.delta/110))), "units")

    def _bind_to_mousewheel(self, event):
        if platform == "linux" or platform == "linux2":
            self.canvas.bind_all("<MouseWheel>", fp(self._on_mousewheel, scroll=-1))
            self.canvas.bind_all("<Button-5>", fp(self._on_mousewheel, scroll=1))
        else:
            self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):

        if platform == "linux" or platform == "linux2":
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.unbind_all("<MouseWheel>")

class Main_Page:
    def __init__(self,master_frame):
        """
        FRAMES
        """
        self.frame_ids=dict()
        self.master_frame=master_frame
        self.Menu_Frame=ct.CTkFrame(master=self.master_frame)
        self.Menu_Frame.pack(side=TOP,fill=X)

        self.Info_Frame=ct.CTkFrame(self.master_frame)
        self.Info_Frame.pack(side=TOP,fill=BOTH,expand=1)

        self.Scrollview_Frame_1=VerticalScrolledFrame(self.Info_Frame)
        self.Scrollview_Frame_1.pack(side=TOP,fill=BOTH,expand=TRUE)
        self.ui_create()

        self.Search_variable=ct.StringVar()
        self.Search_variable.set('')


        self.Add=ct.CTkButton(master=self.Menu_Frame,text="+Add",command=self.Add_Student_launch)
        self.Add.pack(side=LEFT,padx=2)
        self.Search_Label=ct.CTkLabel(master=self.Menu_Frame,text="Search")
        self.Search_Label.pack(side=LEFT)
        self.Search_Entry=ct.CTkEntry(self.Menu_Frame,textvariable=self.Search_variable,placeholder_text="Enter Phone Number")
        self.Search_Entry.pack(side=LEFT,fill=X,expand=TRUE)
        self.Search_Entry.bind('<Return>',self.Search_Enter_key)
        self.Search_button=ct.CTkButton(self.Menu_Frame,text="Search",command=self.Search_Data)
        self.Search_button.pack(side=LEFT,padx=2)
        self.Settings=ct.CTkButton(self.Menu_Frame,text="About",command=self.on_settings)
        self.Settings.pack(side=LEFT,padx=2)

    def Search_Enter_key(self,e):
        self.Search_Data()

    def Search_Data(self):
        value=self.Search_variable.get()
        if value.isdigit():
            Matched_Regno=OP.Search_Customer(value)
            if len(Matched_Regno)!=0:
                for x in Matched_Regno:
                    for y in x:
                        self.ViewPanel=ct.CTkToplevel(self.master_frame)
                        View_Student(self.ViewPanel,self.master_frame,self,y)
            else:
                self.Search_variable.set(value="")
                Error_message(self.master_frame,"Phone Number not Found!")
            
        else:
            self.Search_variable.set(value="")
            Error_message(self.master_frame,"Enter the mobile number to search!")
    
    def on_settings(self):
        self.SettingsPanel=ct.CTkToplevel(self.master_frame)
        Settings_Page(self.SettingsPanel)

    def Add_Student_launch(self):
        
        self.addstudent=ct.CTkToplevel(self.master_frame)
        Add_Student(self.addstudent,self,0)
        
    def Edit_buton(self,buton):
        self.edit_student=ct.CTkToplevel(self.master_frame)
        Add_Student(self.edit_student,self,1,buton)
    
    def Data_viewer(self,btn_id,Ph_no,Name,Tamnt,Pamnt,sideinframe=BOTTOM):
        self.Info_bar=ct.CTkFrame(self.Scrollview_Frame_1.interior)
        self.Info_bar.pack(side=sideinframe,fill=X,expand=TRUE,pady=6,padx=2)
        self.frame_ids[f"{btn_id}"]=self.Info_bar
        self.PhoneNo=ct.CTkLabel(self.Info_bar,text=f"{Ph_no}")
        self.PhoneNo.pack(side=LEFT)
        self.Name_label=ct.CTkLabel(self.Info_bar,text=f"{Name}")
        self.Name_label.pack(side=LEFT)

        self.Totalamnt_label=ct.CTkLabel(self.Info_bar,text=F"Total Amount:{Tamnt}")
        self.Totalamnt_label.pack(side=LEFT)
        self.Amount_label=ct.CTkLabel(self.Info_bar,text=f"Paid:{Pamnt}")
        self.Amount_label.pack(side=LEFT)
        self.Balance_label=ct.CTkLabel(self.Info_bar,text=f"Balance:{int(Tamnt)-int(Pamnt)}")
        self.Balance_label.pack(side=LEFT)

        self.Edit_button=ct.CTkButton(self.Info_bar,text="Edit",command=fp(self.Edit_buton,f"{btn_id}"))
        self.Edit_button.pack(side=LEFT,padx=3)

        self.Delete_button=ct.CTkButton(self.Info_bar,text="Delete",command=fp(self.Delete_data_btn,f"{btn_id}",0))
        self.Delete_button.pack(side=LEFT,padx=3)
 
    def ui_create(self):
        for x in reversed(OP.Get_Full_Data()):
            self.Data_viewer(x[0],x[2],x[1],x[4],x[5],BOTTOM)
            
    def Delete_data_btn(self,Regno,modes):
        self.Confirmation=ct.CTkToplevel(self.master_frame)
        self.Confirmation.title("Delete")
        self.Confirmation.grab_set()
        self.Confirmation.iconbitmap("./Icons/close.ico")
        Confirm_label=ct.CTkLabel(master=self.Confirmation,text="Confirm to delete this?")
        Confirm_label.pack(side=TOP)
        ButtonFrame=ct.CTkFrame(master=self.Confirmation)
        ButtonFrame.pack(side=TOP)
        Confirm_btn=ct.CTkButton(master=ButtonFrame,text="Delete",command=fp(self.Confirm_delete,Regno,modes))
        Cancel_btn=ct.CTkButton(master=ButtonFrame,text="Cancel",fg_color=None,command=self.Cancel_delete,border_width=3)
        Cancel_btn.pack(side=RIGHT,padx=5)
        Confirm_btn.pack(side=RIGHT,padx=5)
        
    def Cancel_delete(self):
        self.Confirmation.destroy()

    def Confirm_delete(self,Regno,modes):
        """
        MODES
        0-Mainpage Button
        1-Viewpage Button
        """
        self.Confirmation.destroy()
        Status=OP.Delete_customer(Regno)
        if modes==0:
            if Status==True:
                self.frame_ids[Regno].destroy()
            else:
                Error_message(self.master_frame,"Deletion Error")
        else:
            if Status==True:
                self.frame_ids.keys()
                if str(Regno) in self.frame_ids.keys():
                    self.frame_ids[str(Regno)].destroy()
                    self.ViewPanel.destroy()
            else:
                Error_message(self.master_frame,"Deletion Error")
                    
class Add_Student:
    def __init__(self,master,another_self,modes,keyid=None):
        """
        VARIABLES
        modes:
        0-add
        1-Edit
        """
        self.another_self=another_self
        self.windowusemode=modes
        self.primarykey=keyid
        self.T_amount=IntVar(value=0)
        self.main_frame=master
        self.main_frame.grab_set()
        self.main_frame.geometry("500x200")
        self.main_frame.minsize(500,200)
        self.main_frame.maxsize(500,250)
        self.main_frame.resizable(False,True)
        self.Name_str=StringVar(value="")
        self.Phone_str=StringVar(value="")
        self.AmntPaid_str=StringVar(value="")
        self.Warning_list=dict()
        self.height=200
        
        if modes==1:
            self.main_frame.iconbitmap("./Icons/draw.ico")
            self.main_frame.title("Edit")
            data_known=OP.Get_Data(keyid)
            self.T_amount.set(data_known[0][6])
            self.Name_str.set(f"{data_known[0][1]}")
            self.Phone_str.set(f"{data_known[0][2]}")
            self.AmntPaid_str.set(f"{data_known[0][6]}")

        else:
            self.main_frame.iconbitmap("./Icons/add.ico")
            self.main_frame.title("Add")
        """
        FRAMES
        """
        self.Main_Frame_Add=ct.CTkFrame(master=self.main_frame)
        self.Main_Frame_Add.pack(side=TOP)
        self.Name_list=ct.CTkFrame(master=self.Main_Frame_Add,fg_color=None)
        self.Name_list.pack(side=LEFT)
        self.Text_Input_List=ct.CTkFrame(master=self.Main_Frame_Add,fg_color=None)
        self.Text_Input_List.pack(side=RIGHT)
        self.ButtonFrame=ct.CTkFrame(master=self.main_frame,width=500,fg_color=None)
        self.ButtonFrame.pack(side=TOP,fill=X)
        self.WarningPanel=ct.CTkFrame(master=self.main_frame,fg_color="Red")
        """
        WIDGETS
        """
        #Label
        self.Name_label=ct.CTkLabel(master=self.Name_list,text="Name",width=200,height=35,text_font=("lucida",13))
        self.Name_label.pack(side=TOP)
        self.Mobleno_Lablel=ct.CTkLabel(master=self.Name_list,text="Mobile No",width=200,height=35,text_font=("lucida",13))
        self.Mobleno_Lablel.pack(side=TOP)
        self.Amnt_Lablel=ct.CTkLabel(master=self.Name_list,text="Amount Paid",width=200,height=35,text_font=("lucida",13))
        self.Amnt_Lablel.pack(side=TOP)
        self.T_amount_label=ct.CTkLabel(master=self.Name_list,text="Total Amount",width=200,height=35,text_font=("lucida",13))
        self.T_amount_label.pack(side=TOP)

        #EntryBox
        self.Name_Entry=ct.CTkEntry(master=self.Text_Input_List,textvariable=self.Name_str,width=275,height=35)
        self.Name_Entry.pack(side=TOP)
        self.Mobileno_Entry=ct.CTkEntry(master=self.Text_Input_List,textvariable=self.Phone_str,width=275,height=35)
        self.Mobileno_Entry.pack(side=TOP)
        self.AmntPaid_Entry=ct.CTkEntry(master=self.Text_Input_List,textvariable=self.AmntPaid_str,width=275,height=35)
        self.AmntPaid_Entry.pack(side=TOP)
        self.T_amount_Entry=ct.CTkEntry(master=self.Text_Input_List,textvariable=self.T_amount,width=275,height=35)
        self.T_amount_Entry.pack(side=TOP)

        #Button
        self.print_btn=ct.CTkButton(self.ButtonFrame,text='Print',command=self.on_print_press,corner_radius=8,text_font=("lucida",13))
        self.Cancel=ct.CTkButton(master=self.ButtonFrame,text='Cancel',command=self.on_press_cancel,corner_radius=8,text_font=("lucida",13))
        self.Cancel.pack(side=RIGHT,padx=5)
        self.Save=ct.CTkButton(master=self.ButtonFrame,text="Save",command=self.on_press_save,text_font=("lucida",13))
        self.Save.pack(side=RIGHT,padx=5)
        self.print_btn.pack(side=RIGHT,padx=5)

    """
    FUNCTIONS
    """
    def on_print_press(self):
        if self.check_field_empty and self.check_field_int:
        
            bal=int(self.T_amount.get())-int(self.AmntPaid_str.get())

            OP.Print_page(self.Name_str.get(),self.Phone_str.get(),self.AmntPaid_str.get(),bal)

    def check_field_empty(self):
        x=[self.Name_str.get(),self.Phone_str.get(),self.AmntPaid_str.get()]
        for i in x:
            if i=='' or self.T_amount.get()==0:
                if "field empty" not in self.Warning_list.keys():
                    self.height+=20
                    self.main_frame.geometry(f"500x{self.height}")
                    self.WarningPanel.pack(side=TOP,fill=X)
                    self.Warning_lable_Field=ct.CTkLabel(master=self.WarningPanel,text="All Fields are Required!",text_color="white",anchor="w")
                    self.Warning_list["field empty"]=self.Warning_lable_Field
                    self.Warning_lable_Field.pack(side=TOP)
                    return False
        if "field empty" in self.Warning_list.keys():
            self.height-=20
            self.Warning_list["field empty"].destroy()
            self.main_frame.geometry(f"500x{self.height}")
            del self.Warning_list["field empty"]
        return True

    def check_field_int(self):
        x=[self.Phone_str.get(),self.AmntPaid_str.get()]
        for i in x:
            if i.isdigit()==False:
                if "field int" not in self.Warning_list:
                    self.height+=20
                    self.main_frame.geometry(f"500x{self.height}")
                    self.WarningPanel.pack(side=TOP,fill=X)
                    Warning_lable_Int=ct.CTkLabel(master=self.WarningPanel,text="Phone no and Amount no should only have int!",text_color="white")
                    self.Warning_list["field int"]=Warning_lable_Int
                    Warning_lable_Int.pack(side=TOP)
                    return False
                else:
                    return False
        if "field int" in self.Warning_list.keys():
            self.height-=20
            self.Warning_list["field int"].destroy()
            self.main_frame.geometry(f"500x{self.height}")
            del self.Warning_list["field int"]
        return True
    
    def on_press_save(self):
        if self.windowusemode==1:
            Newdata=[self.primarykey,self.Name_str.get(),self.Phone_str.get(),datetime.now(),self.T_amount.get(),self.AmntPaid_str.get()]
            Olddata=OP.Get_Data(self.primarykey)

            column=0
            changes=0
            while column<=5:

                if str(Newdata[column])!=str(Olddata[0][column]):

                    changes+=1
                    Status=OP.update_db(self.primarykey,column,Newdata[column])
                    if Status==True:
                        pass
                    else:
                        self.main_frame.destroy()
                        break
                

                column+=1
            
            if changes>1:
                self.another_self.frame_ids[self.primarykey].destroy()
                del self.another_self.frame_ids[self.primarykey]

                Main_Page.Data_viewer(self.another_self,self.primarykey,self.Phone_str.get(),self.Name_str.get(),self.T_amount.get(),self.AmntPaid_str.get(),BOTTOM)
                self.main_frame.destroy()
            else:
                self.main_frame.destroy()

        else:
            if self.check_field_empty() and self.check_field_int():
                if OP.Add_customer(self.Name_str.get(),self.Phone_str.get(),self.AmntPaid_str.get(),self.T_amount.get())==True:

                    Mregno=OP.Max_Regno()
                    Frame_dlt_keys=list(self.another_self.frame_ids.keys())
                    if len(Frame_dlt_keys)>24:
                        key_frame=Frame_dlt_keys[0]
                        self.another_self.frame_ids[str(key_frame)].destroy()
                        del self.another_self.frame_ids[str(key_frame)]

                    Main_Page.Data_viewer(self.another_self,int(Mregno[0]),self.Phone_str.get(),self.Name_str.get(),self.T_amount.get(),self.AmntPaid_str.get(),BOTTOM)
                    self.main_frame.destroy()
                else:
                    Error_message(self.main_frame,"Record Failed to Add!")

    def on_press_cancel(self):
        self.main_frame.destroy()

class View_Student:
    def __init__(self,master,MainPage_Frame,another_self,Regno):
        self.main_frame=master
        self.main_frame.grab_set()
        self.Main_Page=MainPage_Frame
        self.another_self=another_self
        self.main_frame.resizable(False,False)

        self.another_self.Search_variable.set('')
        self.RegistryNO=Regno
        self.data=OP.Get_Data(Regno)[0]
        self.main_frame.title(self.data[1])
        self.main_frame.iconbitmap("./Icons/account.ico")
        self.Name=self.data[1]
        self.Phno=self.data[2]
        self.Tamnt=self.data[4]
        self.Pamnt=self.data[5]
        self.pamnt_label=StringVar(value=self.Pamnt)
        self.bal_label=StringVar(value=self.data[6])
        

        """
        #Frames

        """
        self.LabelFrame=ct.CTkFrame(self.main_frame)
        self.LabelFrame.pack(side=TOP,fill=X)
        self.Col1=ct.CTkFrame(self.LabelFrame,fg_color=None)
        self.Col2=ct.CTkFrame(self.LabelFrame,fg_color=None)
        self.Col1.pack(side=LEFT,fill=X)
        self.Col2.pack(side=LEFT,fill=X)
        self.ButtonFrame=ct.CTkFrame(self.main_frame)
        self.ButtonFrame.pack(side=TOP,pady=5)

        """"
        #Widgets
        """
        self.NameTag=ct.CTkLabel(self.Col1,text="Name",text_font=("lucida",13))
        self.PhonenoTag=ct.CTkLabel(self.Col1,text="Mobile Number",text_font=("lucida",13))
        self.PamntTag=ct.CTkLabel(self.Col1,text="Paid Amount",text_font=("lucida",13))
        self.TamntTag=ct.CTkLabel(self.Col1,text="Total Amount",text_font=("lucida",13))
        self.BalTag=ct.CTkLabel(self.Col1,text="Balance",text_font=("lucida",13))
        self.NameTag.   pack(side=TOP,fill=X)
        self.PhonenoTag.pack(side=TOP,fill=X)
        self.TamntTag.  pack(side=TOP,fill=X)
        self.PamntTag.  pack(side=TOP,fill=X)
        self.BalTag.pack(side=TOP,fill=X)

        self.Namelabel=ct.CTkLabel( self.Col2,text=f"{self.Name}",text_font=("lucida",13))
        self.Phnolabel=ct.CTkLabel( self.Col2,text=f"{self.Phno}",text_font=("lucida",13))
        self.Tamntlabel=ct.CTkLabel(self.Col2,text=f"{self.Tamnt}",text_font=("lucida",13))
        self.Pamntlabel=ct.CTkLabel(self.Col2,textvariable=self.pamnt_label,text_font=("lucida",13))
        self.Ballabel=ct.CTkLabel(self.Col2,textvariable=self.bal_label,text_font=("lucida",13))
        self.Namelabel. pack(side=TOP,fill=X)
        self.Phnolabel. pack(side=TOP,fill=X)
        self.Tamntlabel.pack(side=TOP,fill=X)
        self.Pamntlabel.pack(side=TOP,fill=X)
        self.Ballabel.pack(side=TOP,fill=X)


        self.Paybtn=ct.CTkButton(self.ButtonFrame,text="Pay",command=self.Pay_Button_press)
        self.Deletebtn=ct.CTkButton(self.ButtonFrame,text="Delete",command=fp(self.Delete_Button_press,self.data[0]))
        self.Editbtn=ct.CTkButton(self.ButtonFrame,text="Edit",command=fp(self.Edit_Button_press,self.data[0]))
        self.Print_btn=ct.CTkButton(self.ButtonFrame,text='Print',command=self.on_print_press,corner_radius=8,text_font=("lucida",13))
        self.Paybtn.pack(side=RIGHT,padx=3)
        self.Deletebtn.pack(side=RIGHT,padx=3)
        self.Editbtn.pack(side=RIGHT,padx=3)
        self.Print_btn.pack(side=RIGHT,padx=3)
    
    def Pay_Button_press(self):
        Paywindow=ct.CTkInputDialog(self.main_frame,title="Pay",text="Pay Amount")
        amnt=Paywindow.get_input()
        if amnt.isdigit():
            self.Pamnt=int(self.Pamnt)+int(amnt) 
            OP.update_db(self.RegistryNO,6,self.Pamnt)
            OP.update_db(self.RegistryNO,3,datetime.now())
            self.pamnt_label.set(value=self.Pamnt)
            self.bal_label.set(self.Tamnt-self.Pamnt)
            if str(self.RegistryNO) in self.another_self.frame_ids.keys():
                self.another_self.frame_ids[str(self.RegistryNO)].destroy()
                del self.another_self.frame_ids[str(self.RegistryNO)]

            Main_Page.Data_viewer(self.another_self,self.RegistryNO,self.Phno,self.Name,self.Tamnt,self.Pamnt)
            

    
    def on_print_press(self):
        bal=self.Tamnt-self.Pamnt
        OP.Print_page(self.Name,self.Phno,self.Tamnt,bal)

    def Delete_Button_press(self,RegNO):
        Main_Page.Delete_data_btn(self.another_self,RegNO,1)

    def Edit_Button_press(self,RegNO):
        
        self.main_frame.destroy()
        self.Edit_Frame=ct.CTkToplevel(self.Main_Page)
        Add_Student(self.Edit_Frame,self.another_self,1,str(RegNO))

class Settings_Page:
    def __init__(self,masterframe):
        self.main_frame=masterframe
        self.main_frame.grab_set()
        self.main_frame.iconbitmap("./Icons/attention.ico")
        self.main_frame.title('About')
        self.main_frame.resizable(False,False)

        
        """
        FRAMES
        """

        self.AboutFrame=ct.CTkFrame(self.main_frame)

        self.AboutFrame.pack(side=TOP,fill=X)

        """
        WIDGETS
        """
        
        
        self.About_Label=ct.CTkLabel(self.AboutFrame,text="About\n Created By:Harikrishna A\nGithub:Glitch-hash01",text_font=("lucida",9))    
        self.About_Label.pack(side=TOP)


        self.OKbtn=ct.CTkButton(self.AboutFrame,text="OK",command=self.Everything_OK)
        self.OKbtn.pack(side=BOTTOM)   
    def Everything_OK(self):
        self.main_frame.destroy()

class Error_message:
    def __init__(self,masterframe,Error_msg):
        self.Message_Frame=ct.CTkToplevel(masterframe)
        self.Message_Frame.title("WARNING")
        self.Message_Frame.iconbitmap("./Icons/attention.ico")
        self.Message_Frame.geometry("300x50")
        self.Message_Frame.resizable(False,False)
        self.Message_Frame.grab_set()

        self.Error_label=ct.CTkLabel(self.Message_Frame,text=Error_msg)
        self.Error_label.pack(side=TOP)

        self.OKbtn=ct.CTkButton(self.Message_Frame,text="OK",command=self._OK_)
        self.OKbtn.pack(side=TOP)

    def _OK_(self):
        self.Message_Frame.destroy()

if __name__=="__main__":
    root=ct.CTk()
    root.set_appearance_mode("Light")
    root.minsize(700,300)
    root.state("zoomed")
    root.title('Accounting Software')
    root.iconbitmap('./Icons/Logo.ico')
    Main_Page(root)
    root.mainloop()


