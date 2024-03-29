import tkinter as tk
import time
import threading
import subprocess
from tkinter import ttk

root = tk.Tk()
root.title('Windows Server Setup')
root.geometry('500x500')

# 添加自定義樣式來美化按鈕
style = ttk.Style()
style.configure('Custom.TButton', font=('Helvetica', 12), foreground='blue', padding=5)
style.configure('Red.TButton', font=('Helvetica', 12), foreground='red', padding=5)
style.configure('Green.TButton', font=('Helvetica', 12), foreground='green', padding=5)

def powershell(command):
    subprocess.run(["powershell.exe", command])

#-----<DHCP>-----

#-----<DHCP_Install>-----
def DHCP_Install_Click():
    DHCP_install_thread = threading.Thread(target=installing_DHCP)
    DHCP_install_thread.start()
    DHCP_Install.config(text='Installing')

def installing_DHCP():
    powershell("Install-WindowsFeature -Name 'DHCP' –IncludeManagementTools")
    DHCP_complete_thread = threading.Thread(target=Func_DHCP_complete)
    DHCP_complete_thread.start()

def Func_DHCP_complete():
    DHCP_Install.config(text="Finished")  
    time.sleep(3)
    DHCP_Install.config(text="Install DHCP Feature")  

#-----</DHCP_Install>-----
    
#-----<DHCP_Uninstall>-----
def DHCP_Uninstall_Click():
    DHCP_Uninstall_thread = threading.Thread(target=Uninstalling_DHCP)
    DHCP_Uninstall_thread.start()
    DHCP_Uninstall.config(text='Uninstalling')

def Uninstalling_DHCP():
    powershell("Uninstall-WindowsFeature -Name 'DHCP' –IncludeManagementTools")
    DHCP_complete_thread = threading.Thread(target=Func_UnDHCP_complete)
    DHCP_complete_thread.start()

def Func_UnDHCP_complete():
    DHCP_Uninstall.config(text="Finished")  
    time.sleep(3)
    DHCP_Uninstall.config(text="Uninstall DHCP Feature")  
#-----</DHCP_Uninstall>-----
    
#-----<DHCP_Setup>-----
def DHCP_Setup_Click():
    #-----<Read、Setup and close>-----
    def DHCP_Finish_Button():
        DHCP_Setup_thread = threading.Thread(target=read_DHCP_input)
        DHCP_Setup_thread.start()
        read_input.config(text="Please Wait")

    def read_DHCP_input():
        StartRange=StartRangeentry.get()
        EndRange=EndRangeentry.get()
        SubnetMask=SubnetMaskentry.get()
        ScopeName=ScopeNameentry.get()
        DNS_Address=DNS_Addressentry.get()
        Router=Routerentry.get()
        #<Scope id calculate>
        r=StartRange.split(".")
        ScopeID=""
        for i in range(3):
            ScopeID+=r[i]
            ScopeID+="."
        ScopeID+="0"
        #</Scope id calculate>
        AddScope="Add-DhcpServerV4Scope -Name "+ScopeName+" -StartRange "+StartRange+" -EndRange "+EndRange+" -Subnetmask "+SubnetMask
        powershell(AddScope)
        SetDHCPDNS="Set-DhcpServerv4OptionValue -ScopeId "+ScopeID+" -OptionId 6 -Value "+DNS_Address
        powershell(SetDHCPDNS)
        SetDHCPRouter="Set-DhcpServerv4OptionValue -ScopeId "+ScopeID+" -Router "+Router
        powershell(SetDHCPRouter)
        DHCP_Setup_Window.destroy()
        DHCP_Setup_Window.update()
    
    #-----</Read、Setup and close>-----

    #-----<Just close>-----
    def DHCP_Setup_Exit():
        DHCP_Setup_Window.destroy()
        DHCP_Setup_Window.update()
    #-----</Just close>-----

    DHCP_Setup_Window = tk.Toplevel(root)
    DHCP_Setup_Window.geometry("500x500")
    # 設置窗口邊框樣式
    DHCP_Setup_Window.configure(bg='white')
    DHCP_Setup_Window.attributes('-alpha', 0.9)
    DHCP_Setup_Window.attributes('-topmost', 'true')

    #<Entrys>
    StartRangelabel = tk.Label(DHCP_Setup_Window, text='StartRange:')
    StartRangelabel.grid(row=0, column=0)
    StartRangeentry = tk.Entry(DHCP_Setup_Window)
    StartRangeentry.grid(row=0, column=1)
    EndRangelabel = tk.Label(DHCP_Setup_Window, text='EndRange:')
    EndRangelabel.grid(row=1, column=0)
    EndRangeentry = tk.Entry(DHCP_Setup_Window)
    EndRangeentry.grid(row=1, column=1)
    SubnetMasklabel = tk.Label(DHCP_Setup_Window, text='SubnetMask:')
    SubnetMasklabel.grid(row=2, column=0)
    SubnetMaskentry = tk.Entry(DHCP_Setup_Window)
    SubnetMaskentry.grid(row=2, column=1)
    ScopeNamelabel = tk.Label(DHCP_Setup_Window, text='ScopeName:')
    ScopeNamelabel.grid(row=3, column=0)
    ScopeNameentry = tk.Entry(DHCP_Setup_Window)
    ScopeNameentry.grid(row=3, column=1)
    DNS_Addresslabel = tk.Label(DHCP_Setup_Window, text='DNS Address:')
    DNS_Addresslabel.grid(row=4, column=0)
    DNS_Addressentry = tk.Entry(DHCP_Setup_Window)
    DNS_Addressentry.grid(row=4, column=1)
    Routerlabel = tk.Label(DHCP_Setup_Window, text='Router IP:')
    Routerlabel.grid(row=5, column=0)
    Routerentry = tk.Entry(DHCP_Setup_Window)
    Routerentry.grid(row=5, column=1)
    #</Entrys>
 
    Exit=ttk.Button(DHCP_Setup_Window, text="Exit", command=DHCP_Setup_Exit, style='Red.TButton')
    Exit.grid(row=6,column=0,padx=20)
    read_input=ttk.Button(DHCP_Setup_Window, text="Finish", command=DHCP_Finish_Button, style='Green.TButton')
    read_input.grid(row=6,column=1)    
    #-----</DHCP_Setup>-----

#----</DHCP>-----
def Remove_DHCP_Scope_Click():

    def DHCP_Setup_Exit():
        Remove_DHCP_Scope_Window.destroy()
        Remove_DHCP_Scope_Window.update()

    def DHCP_Finish_Button():
        ScopeID=ScopeIDentry.get()
        command="Remove-DhcpServerv4Scope -ScopeId "+ScopeID
        powershell(command)

    Remove_DHCP_Scope_Window = tk.Toplevel(root)
    Remove_DHCP_Scope_Window.geometry("500x500")
    ScopeIDlabel = tk.Label(Remove_DHCP_Scope_Window, text='ScopeID:')
    ScopeIDlabel.grid(row=0, column=0)
    ScopeIDentry = tk.Entry(Remove_DHCP_Scope_Window)
    ScopeIDentry.grid(row=0, column=1)
    Exit=ttk.Button(Remove_DHCP_Scope_Window, text="Exit", command=DHCP_Setup_Exit, style='Red.TButton')
    Exit.grid(row=6,column=0,padx=20)
    read_input=ttk.Button(Remove_DHCP_Scope_Window, text="Finish", command=DHCP_Finish_Button, style='Green.TButton')
    read_input.grid(row=6,column=1) 
#----<DNS>-----
    #-----<DNS_Install>

def DNS_Install_Click():
    DNS_install_thread = threading.Thread(target=installing_DNS)
    DNS_install_thread.start()
    DNS_Install.config(text='Installing')

def installing_DNS():
    powershell("Install-WindowsFeature -Name 'DNS' –IncludeManagementTools")
    DNS_complete_thread = threading.Thread(target=Func_DNS_complete)
    DNS_complete_thread.start()


def Func_DNS_complete():
    DNS_Install.config(text="Finished")  
    time.sleep(3)
    DNS_Install.config(text="Install DNS Feature")  
    
    #-----</DNS_Install>-----

    #-----<DNS_Uninstall>

def DNS_Uninstall_Click():
    DNS_Uninstall_thread = threading.Thread(target=Uninstalling_DNS)
    DNS_Uninstall_thread.start()
    DNS_Uninstall.config(text='Uninstalling')

def Uninstalling_DNS():
    powershell("Uninstall-WindowsFeature -Name 'DNS' –IncludeManagementTools")
    DNS_complete_thread = threading.Thread(target=Func_UnDNS_complete)
    DNS_complete_thread.start()


def Func_UnDNS_complete():
    DNS_Uninstall.config(text="Finished")  
    time.sleep(3)
    DNS_Uninstall.config(text="Uninstall DNS Feature")  
    
    #-----</DNS_Uninstall>-----

    #-----<DNS_Main_Window>-----
def DNS_Setup_click():

        #-----<Foward lookup zone>-----
    def Foward_Lookup_Zone_Click():
            #-----<Primary Zone Setting>-----
        def Add_Primary_Button_Click():
                #-----<Add>-----
            def Add_Primary_Zone_Click():
                DNS_install_thread = threading.Thread(target=Adding_Zone)
                DNS_install_thread.start()
                Add_Primart_Zone_input.config(text="Please Wait")
            def Adding_Zone():
                ZoneName=ZoneNameEntry.get()
                ZoneFile=ZoneName+".dns"
                command="Add-DnsServerPrimaryZone -Name "+ZoneName+" -ZoneFile "+ZoneFile
                powershell(command)
                Add_Primary_Button_Window.destroy()
                #-----</Add>-----
                
            Add_Primary_Button_Window=tk.Toplevel(Foward_Lookup_Zone_Window)
            Add_Primary_Button_Window.geometry("200x200")
            ZoneNamelabel=tk.Label(Add_Primary_Button_Window,text="Zone Name")
            ZoneNamelabel.grid(row=0,column=0)
            ZoneNameEntry=tk.Entry(Add_Primary_Button_Window)
            ZoneNameEntry.grid(row=0,column=1)
            Add_Primart_Zone_input=tk.Button(Add_Primary_Button_Window,text="Finish",command=Add_Primary_Zone_Click)
            Add_Primart_Zone_input.grid(row=1,column=1)
            #-----</Primary Zone Setting>-----

            #----<DNS Record>----
        def Add_DNS_Record_Click():
                #----<ADD DNS Record>----
            def DNS_Record_input_Click():
                tmp=Set_Record_Type.get()
                if tmp=="A":
                    def A_input_Click():
                        DNS_install_thread = threading.Thread(target=installing_DNS_A)
                        DNS_install_thread.start()
                        A_input.config(text="Please Wait")
                    def installing_DNS_A():
                        zone=Set_Zone_Entry.get()
                        name=Name_Entry.get()
                        IPv4Address=IPv4Address_Entry.get()
                        command="Add-DnsServerResourceRecordA -Name "+name+" -ZoneName "+zone+" -IPv4Address "+IPv4Address
                        powershell(command)
                        Add_A_Record_Window.destroy()
                    Add_A_Record_Window=tk.Toplevel(Add_DNS_Record_Window)
                    Add_A_Record_Window.geometry("200x200")
                    Name_Label=tk.Label(Add_A_Record_Window,text="Name:")
                    Name_Label.grid(row=0,column=0)
                    Name_Entry=tk.Entry(Add_A_Record_Window)
                    Name_Entry.grid(row=0,column=1)
                    IPv4Address_Label=tk.Label(Add_A_Record_Window,text="IPv4Address:")
                    IPv4Address_Label.grid(row=1,column=0)
                    IPv4Address_Entry=tk.Entry(Add_A_Record_Window)
                    IPv4Address_Entry.grid(row=1,column=1)
                    A_input=tk.Button(Add_A_Record_Window,text="Finish",command=A_input_Click)
                    A_input.grid(row=2,column=1)
                elif tmp=="AAAA":
                    def AAAA_input_Click():
                        DNS_install_thread = threading.Thread(target=installing_DNS_AAAA)
                        DNS_install_thread.start()
                        AAAA_input.config(text="Please Wait")
                    def installing_DNS_AAAA():
                        zone=Set_Zone_Entry.get()
                        name=Name_Entry.get()
                        IPv6Address=IPv6Address_Entry.get()
                        command="Add-DnsServerResourceRecordAAAA -Name "+name+" -ZoneName "+zone+" -IPv6Address "+IPv6Address
                        powershell(command)
                        Add_AAAA_Record_Window.destroy()
                    Add_AAAA_Record_Window=tk.Toplevel(Add_DNS_Record_Window)
                    Add_AAAA_Record_Window.geometry("200x200")
                    Name_Label=tk.Label(Add_AAAA_Record_Window,text="Name:")
                    Name_Label.grid(row=0,column=0)
                    Name_Entry=tk.Entry(Add_AAAA_Record_Window)
                    Name_Entry.grid(row=0,column=1)
                    IPv6Address_Label=tk.Label(Add_AAAA_Record_Window,text="IPv6Address:")
                    IPv6Address_Label.grid(row=1,column=0)
                    IPv6Address_Entry=tk.Entry(Add_AAAA_Record_Window)
                    IPv6Address_Entry.grid(row=1,column=1)
                    AAAA_input=tk.Button(Add_AAAA_Record_Window,text="Finish",command=AAAA_input_Click)
                    AAAA_input.grid(row=2,column=1)
                else:
                    def CName_input_Click():
                        DNS_install_thread = threading.Thread(target=installing_DNS_CName)
                        DNS_install_thread.start()
                        CName_input.config(text="Please Wait")
                    def installing_DNS_CName():
                        zone=Set_Zone_Entry.get()
                        name=Name_Entry.get()
                        HostNameAlias=HostNameAlias_Entry.get()
                        command="Add-DnsServerResourceRecordCName -Name "+name+" -ZoneName "+zone+" -HostNameAlias "+HostNameAlias
                        powershell(command)
                        Add_CName_Record_Window.destroy()
                    Add_CName_Record_Window=tk.Toplevel(Add_DNS_Record_Window)
                    Add_CName_Record_Window.geometry("200x200")
                    Name_Label=tk.Label(Add_CName_Record_Window,text="Name:")
                    Name_Label.grid(row=0,column=0)
                    Name_Entry=tk.Entry(Add_CName_Record_Window)
                    Name_Entry.grid(row=0,column=1)
                    HostNameAlias_Label=tk.Label(Add_CName_Record_Window,text="HostNameAlias:")
                    HostNameAlias_Label.grid(row=1,column=0)
                    HostNameAlias_Entry=tk.Entry(Add_CName_Record_Window)
                    HostNameAlias_Entry.grid(row=1,column=1)
                    CName_input=tk.Button(Add_CName_Record_Window,text="Finish",command=CName_input_Click)
                    CName_input.grid(row=2,column=1)

            Add_DNS_Record_Window=tk.Toplevel(Foward_Lookup_Zone_Window)
            Add_DNS_Record_Window.geometry("200x200")
            Set_Zone_Label=tk.Label(Add_DNS_Record_Window,text="Set Zone:")
            Set_Zone_Label.grid(row=0,column=0)
            Set_Zone_Entry=tk.Entry(Add_DNS_Record_Window)
            Set_Zone_Entry.grid(row=0,column=1)
            #---<!!!!!!!需合併column!!!!!>---
            Set_Record_Type=ttk.Combobox(Add_DNS_Record_Window,values=["A","AAAA","CName"])
            Set_Record_Type.grid(row=1,column=0)
            DNS_Record_input=tk.Button(Add_DNS_Record_Window,text="Finish",command=DNS_Record_input_Click)
            DNS_Record_input.grid(row=2,column=0)
                #----</ADD DNS Record>----
        def Remove_DNS_Zone_Click():
            def DNS_Finish_Button():
                Zone=ZoneNameentry.get()
                command="Remove-DnsServerZone -Name "+Zone+" -Force"
                powershell(command)
                Remove_DNS_Zone_Window.destroy()
            def DNS_Setup_Exit():
                Remove_DNS_Zone_Window.destroy()
            Remove_DNS_Zone_Window=tk.Toplevel(Foward_Lookup_Zone_Window)
            Remove_DNS_Zone_Window.geometry("200x200")
            ZoneNamelabel = tk.Label(Remove_DNS_Zone_Window, text='ZoneName:')
            ZoneNamelabel.grid(row=0, column=0)
            ZoneNameentry = tk.Entry(Remove_DNS_Zone_Window)
            ZoneNameentry.grid(row=0, column=1)
            Exit=ttk.Button(Remove_DNS_Zone_Window, text="Exit", command=DNS_Setup_Exit, style='Red.TButton')
            Exit.grid(row=6,column=0,padx=20)
            read_input=ttk.Button(Remove_DNS_Zone_Window, text="Finish", command=DNS_Finish_Button, style='Green.TButton')
            read_input.grid(row=6,column=1)            
        def Remove_DNS_Record_Click():
            def DNS_Finish_Button():
                Zone=ZoneNameentry.get()
                Record=RecordNameentry.get()
                type=str(Set_Record_Type.get())
                command="Remove-DnsServerResourceRecord -ZoneName "+Zone+" -Name "+Record+" -RRType "+type+" -Force"
                powershell(command)
                Remove_DNS_Record_Window.destroy()
            def DNS_Setup_Exit():
                Remove_DNS_Record_Window.destroy()
            Remove_DNS_Record_Window=tk.Toplevel(Foward_Lookup_Zone_Window)
            Remove_DNS_Record_Window.geometry("500x500")
            ZoneNamelabel = tk.Label(Remove_DNS_Record_Window, text='ScopeID:')
            ZoneNamelabel.grid(row=0, column=0)
            ZoneNameentry = tk.Entry(Remove_DNS_Record_Window)
            ZoneNameentry.grid(row=0, column=1)
            RecordNamelabel = tk.Label(Remove_DNS_Record_Window, text='RecordName:')
            RecordNamelabel.grid(row=1, column=0)
            RecordNameentry = tk.Entry(Remove_DNS_Record_Window)
            RecordNameentry.grid(row=1, column=1)
            Set_Record_Type=ttk.Combobox(Remove_DNS_Record_Window,values=["A","AAAA","CName"])
            Set_Record_Type.grid(row=2,column=0)
            Exit=ttk.Button(Remove_DNS_Record_Window, text="Exit", command=DNS_Setup_Exit, style='Red.TButton')
            Exit.grid(row=6,column=0,padx=20)
            read_input=ttk.Button(Remove_DNS_Record_Window, text="Finish", command=DNS_Finish_Button, style='Green.TButton')
            read_input.grid(row=6,column=1)            
        Foward_Lookup_Zone_Window=tk.Toplevel(DNS_Setup_Window)
        Foward_Lookup_Zone_Window.geometry("200x200")
        Add_Primary_Zone_Button=tk.Button(Foward_Lookup_Zone_Window,text="Add Primary Zone",command=Add_Primary_Button_Click)
        Add_Primary_Zone_Button.pack()
        Add_DNS_Record_Button=tk.Button(Foward_Lookup_Zone_Window,text="Add DNS Record",command=Add_DNS_Record_Click)
        Add_DNS_Record_Button.pack()
        Remove_DNS_Zone_Button=tk.Button(Foward_Lookup_Zone_Window,text="Remove DNS Zone",command=Remove_DNS_Zone_Click)
        Remove_DNS_Zone_Button.pack()
        Remove_DNS_Record_Button=tk.Button(Foward_Lookup_Zone_Window,text="Remove DNS Recoed",command=Remove_DNS_Record_Click)
        Remove_DNS_Record_Button.pack()       
            #----<DNS Record>----
        
        #-----</Foward lookup zone>-----

        #-----<Reverse lookup zone>-----
    def Reverse_Lookup_Zone_Click():
        Reverse_Lookup_Zone_Window=tk.Toplevel(DNS_Setup_Window)
        Reverse_Lookup_Zone_Window.geometry("200x200")

        def Add_Zone_Button_Click():
            def Add_Reverse_Zone_input_Click():
                NetworkID=NetworkID_Entry.get()
                tmp=NetworkID.split(".")
                zonefile=""
                for i in range(3):
                    zonefile+=tmp[2-i]
                    zonefile+="."
                NetworkID=NetworkID+"/24"
                zonefile+="in-addr.arpa.dns"
                command="Add-DnsServerPrimaryZone -NetworkID "+NetworkID+" -ZoneFile "+zonefile
                powershell(command)
                Add_Zone_Window.destroy()
            Add_Zone_Window=tk.Toplevel(Reverse_Lookup_Zone_Window)
            Add_Zone_Window.geometry("200x200")
            NetworkID_Label=tk.Label(Add_Zone_Window,text="NetworkID:")
            NetworkID_Label.grid(row=0,column=0)
            NetworkID_Entry=tk.Entry(Add_Zone_Window)
            NetworkID_Entry.grid(row=0,column=1)
            Add_Reverse_Zone_input=tk.Button(Add_Zone_Window,text="Finish",command=Add_Reverse_Zone_input_Click)
            Add_Reverse_Zone_input.grid(row=1,column=1)

        def Remove_Zone_Button_Click():
            def Remove_Reverse_Zone_input_Click():
                NetworkID=NetworkID_Entry.get()
                tmp=NetworkID.split(".")
                ID=""
                for i in range(3):
                    ID+=tmp[2-i]
                    ID+="."
                ID+="in-addr.arpa"
                command="Remove-DnsServerZone "+ID+" -Force"
                powershell(command)
                Remove_Zone_Window.destroy()
            Remove_Zone_Window=tk.Toplevel(Reverse_Lookup_Zone_Window)
            Remove_Zone_Window.geometry("200x200")
            NetworkID_Label=tk.Label(Remove_Zone_Window,text="NetworkID:")
            NetworkID_Label.grid(row=0,column=0)
            NetworkID_Entry=tk.Entry(Remove_Zone_Window)
            NetworkID_Entry.grid(row=0,column=1)
            Add_Reverse_Zone_input=tk.Button(Remove_Zone_Window,text="Finish",command=Remove_Reverse_Zone_input_Click)
            Add_Reverse_Zone_input.grid(row=1,column=1)

        Add_Zone_Button=tk.Button(Reverse_Lookup_Zone_Window,text="Add Zone",command=Add_Zone_Button_Click)
        Add_Zone_Button.pack()
        Remove_Zone_Button=tk.Button(Reverse_Lookup_Zone_Window,text="Remove Zone",command=Remove_Zone_Button_Click)
        Remove_Zone_Button.pack()
        #-----</Reverse lookup zone>-----

        #----<DNS Fowarder>----
    def Set_Fowarder_Click():
            #----<Set DNS Fowarder>----
        def input_click():
            DNS_install_thread = threading.Thread(target=Setting_Fowarder)
            DNS_install_thread.start()
            Fowarder_input.config(text="Please Wait")
        def Setting_Fowarder():
            Address=AddressEntry.get()
            command="Set-DnsServerForwarder -IPAddress "+Address
            powershell(command)
            Set_Fowarder_Window.destroy()
            #----</Set DNS Fowarder>----
        Set_Fowarder_Window=tk.Toplevel(DNS_Setup_Window)
        Set_Fowarder_Window.geometry("200x200")
        Addresslabel=tk.Label(Set_Fowarder_Window,text="IPAddress")
        Addresslabel.grid(row=0,column=0)
        AddressEntry=tk.Entry(Set_Fowarder_Window)
        AddressEntry.grid(row=0,column=1)
        Fowarder_input=tk.Button(Set_Fowarder_Window,text="Finish",command=input_click)
        Fowarder_input.grid(row=1,column=1)
        #----</DNS Fowarder>----

    DNS_Setup_Window = tk.Toplevel(root)
    DNS_Setup_Window.geometry("200x200")
    Foward_Lookup_Zone=tk.Button(DNS_Setup_Window,text="Foward Look Zone Settings",command=Foward_Lookup_Zone_Click)
    Foward_Lookup_Zone.pack()
    Reverse_Lookup_Zone=tk.Button(DNS_Setup_Window,text="Reverse Look Zone Settings",command=Reverse_Lookup_Zone_Click)
    Reverse_Lookup_Zone.pack()
    Set_Fowarder=tk.Button(DNS_Setup_Window,text="Set Fowarder",command=Set_Fowarder_Click)
    Set_Fowarder.pack()
        
        
#----</DNS>-----

#----<main>-----
DHCP_Install = ttk.Button(root, text='Install DHCP Feature', command=DHCP_Install_Click, style='Custom.TButton')
DHCP_Install.pack()
DHCP_Uninstall = ttk.Button(root, text='Uninstall DHCP Feature', command=DHCP_Uninstall_Click, style='Custom.TButton')
DHCP_Uninstall.pack()
Setup_DHCP=ttk.Button(root,text="Setup DHCP",command=DHCP_Setup_Click, style='Custom.TButton')
Setup_DHCP.pack()
Remove_DHCP_Scope=ttk.Button(root,text="Remove DHCP Scope",command=Remove_DHCP_Scope_Click, style='Custom.TButton')
Remove_DHCP_Scope.pack()
DNS_Install=ttk.Button(root,text="Install DNS Feature",command=DNS_Install_Click, style='Custom.TButton')
DNS_Install.pack()
DNS_Uninstall=ttk.Button(root,text="Uninstall DNS Feature",command=DNS_Uninstall_Click, style='Custom.TButton')
DNS_Uninstall.pack()
Setup_DNS=ttk.Button(root,text="Setup DNS",command=DNS_Setup_click, style='Custom.TButton')
Setup_DNS.pack()
#----</main>-----
root.mainloop()