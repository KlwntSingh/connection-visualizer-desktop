import tkinter as tk

from controller import services
from config.config import CONFIG
import concurrent.futures
from services.IPInfoService import IPInfo
from beans.PacketBean import Packet

def showappversion():
    toplevel = tk.Toplevel()
    tk.Label(toplevel, text=services["appversion"](), height=0, width=50).pack()


def showauthorinfo():
    toplevel = tk.Toplevel()
    tk.Label(toplevel, text=services["authorinfo"](), height=0, width=50, ).pack()

maxwidth = None
maxheight = None
expiring_map_object = {}
ignored_ip_set_object = {}
should_listen_on_expiring_map_object = False
root = None
ipInfoService = None
snifferThreadId = None
IP_API = CONFIG["IP_API"]
stop_button = None
start_button = None
content_holder_data_frame = None
data_frame = None
executors = None

def sniffer_callback(data):
    global expiring_map_object
    global should_listen_on_expiring_map_object
    global ipInfoService
    global ignored_ip_set_object
    global snifferThreadId
    global executors

    snifferThreadId = data.get("threadId")
    expiring_map_object = data.get("expiring_map", None)
    ignored_ip_set_object = data.get("ignored_ip_set", None)

    executors = concurrent.futures.ProcessPoolExecutor()
    data["executors"] = executors

    ipInfoService = IPInfo(**data)

    should_listen_on_expiring_map_object = True
    response_object_reader()

def get_list_interfaces():
    return services["list_of_interfaces"]()

def app_close_callback():
    global root

    stop_sniffer_thread()

    root.destroy()

def start_sniffer_thread(val):
    global start_button, stop_button

    q = services["startSnifferThread"](val)
    sniffer_callback(q)

    # start_button.config(state='disabled')
    # stop_button.config(state='normal')
    start_button.pack_forget()
    stop_button.pack()

def stop_sniffer_thread():
    global snifferThreadId
    global executors
    global should_listen_on_expiring_map_object
    global start_button, stop_button

    if snifferThreadId:
        services["stopSnifferThread"](snifferThreadId)
    should_listen_on_expiring_map_object = False

    if executors:
        executors.shutdown(wait=True)

    # start_button.config(state='normal')
    # stop_button.config(state='disabled')
    stop_button.pack_forget()
    start_button.pack()

def render_frame():
    global root

    def create_filemenu(parent, root):
        filemenu = tk.Menu(parent)
        filemenu.add_command(label="run with root", command=services["restart_with_root"])
        filemenu.add_command(label="close", command=root.quit)
        return filemenu

    def create_aboutmenu(parent):
        aboutmenu = tk.Menu(parent)
        aboutmenu.add_command(label="version", command=showappversion)
        aboutmenu.add_command(label="author", command=showauthorinfo)
        return aboutmenu

    def create_menu(root):

        menu = tk.Menu(root)
        root.config(menu=menu)

        filemenu = create_filemenu(menu, root)
        aboutmenu = create_aboutmenu(menu)

        menu.add_cascade(label="app", menu=filemenu)
        menu.add_cascade(label="about", menu=aboutmenu)



    def create_root():
        root = tk.Tk()
        root.title(CONFIG["APP_NAME"])
        return root

    root = create_root()
    create_menu(root)
    root.protocol("WM_DELETE_WINDOW", app_close_callback)

    return root

def render_permission_change(root):

    root.mainloop()

def render_content(root):
    global snifferThreadId
    global content_holder_data_frame
    global stop_button
    global start_button
    global maxheight
    global maxwidth

    maxheight = root.winfo_screenheight()
    maxwidth = root.winfo_screenwidth() + 500

    rootFrame = tk.Frame(root, height=maxheight/4, width=maxwidth/2)

    top_bar_frame = tk.Frame(rootFrame, background="white")
    top_bar_frame.pack(fill=None, expand=True)

    dropDownVal = tk.StringVar(top_bar_frame)
    dropDownVal.set("")

    dropDown = tk.OptionMenu(top_bar_frame, dropDownVal, *get_list_interfaces())
    dropDown.pack()

    start_button = tk.Button(top_bar_frame, text="start", command=lambda: start_sniffer_thread(dropDownVal.get()))
    stop_button = tk.Button(top_bar_frame, text="stop", command=lambda: stop_sniffer_thread())


    content_holder_data_frame = tk.Frame(rootFrame,height=maxheight/4, width=maxwidth/2, background="white")

    start_button.pack()
    #stop_button.pack()

    content_holder_data_frame.pack()
    content_holder_data_frame.pack_propagate(0)

    rootFrame.pack()
    scrollbar_interface()

    root.resizable(0, 0)
    root.mainloop()

def scrollbar_interface():
    global content_holder_data_frame
    global data_frame
    global maxwidth

    def myfunction(event):
        nonlocal canvas_around_data_frame
        canvas_around_data_frame.configure(scrollregion=canvas_around_data_frame.bbox("all"))

    content_header_frame = tk.Frame(content_holder_data_frame, width=maxwidth/2)
    content_header_frame.grid(row=0, column=0)

    each_column_width = maxwidth/2/7
    content_header_frame.grid_columnconfigure(0, minsize=each_column_width)
    content_header_frame.grid_columnconfigure(1, minsize=each_column_width)
    content_header_frame.grid_columnconfigure(2, minsize=each_column_width)
    content_header_frame.grid_columnconfigure(3, minsize=each_column_width)
    content_header_frame.grid_columnconfigure(4, minsize=each_column_width)
    content_header_frame.grid_columnconfigure(5, minsize=each_column_width)
    content_header_frame.grid_columnconfigure(6, minsize=each_column_width)

    cell = tk.Label(content_header_frame, text="Server IP Address")
    cell.grid(row=0, column=0)
    cell = tk.Label(content_header_frame, text="Protocol")
    cell.grid(row=0, column=1)
    cell = tk.Label(content_header_frame, text="Interface")
    cell.grid(row=0, column=2)
    cell = tk.Label(content_header_frame, text="Country")
    cell.grid(row=0, column=3)
    cell = tk.Label(content_header_frame, text="State")
    cell.grid(row=0, column=4)
    cell = tk.Label(content_header_frame, text="Region")
    cell.grid(row=0, column=5)
    cell = tk.Label(content_header_frame, text="Domain Name")
    cell.grid(row=0, column=6)

    content_header_frame.pack()

    scroll_and_data_frame = tk.Frame(content_holder_data_frame, width=maxwidth/2)
    scroll_and_data_frame.grid(row=1, column=0)

    canvas_around_data_frame = tk.Canvas(scroll_and_data_frame, width=maxwidth/2)

    data_frame = tk.Frame(canvas_around_data_frame)
    myscrollbar = tk.Scrollbar(scroll_and_data_frame, orient="vertical", command=canvas_around_data_frame.yview)
    canvas_around_data_frame.configure(yscrollcommand=myscrollbar.set)

    myscrollbar.pack(side="right", fill="y")
    canvas_around_data_frame.pack(side="left")
    canvas_around_data_frame.create_window((0, 0), window=data_frame, anchor='nw')
    data_frame.bind("<Configure>", myfunction)

    scroll_and_data_frame.pack()

executor = concurrent.futures.ProcessPoolExecutor()

def populate_other_fields(packet_bean: Packet):

    if not packet_bean.request_fired:
        packet_bean.request_fired = True
        def cb(obj):
            if obj:
                packet_bean.country = obj["country"]
                packet_bean.state = obj["state"]
                packet_bean.region = obj["region"]

        packet_bean.country = "fetching....."
        packet_bean.state = "fetching....."
        packet_bean.region = "fetching....."

        return ipInfoService.getDomainNamesForIP(packet_bean.communicatingIP, cb)

def response_object_reader():
    global root
    global expiring_map_object
    global ignored_ip_set_object
    global should_listen_on_expiring_map_object
    global data_frame
    global maxwidth

    row_index = 0

    for widget in data_frame.winfo_children():
        widget.destroy()

    temp_frame = tk.Frame(data_frame)

    each_column_width = maxwidth / 2 / 7
    temp_frame.grid_columnconfigure(0, minsize=each_column_width)
    temp_frame.grid_columnconfigure(1, minsize=each_column_width)
    temp_frame.grid_columnconfigure(2, minsize=each_column_width)
    temp_frame.grid_columnconfigure(3, minsize=each_column_width)
    temp_frame.grid_columnconfigure(4, minsize=each_column_width)
    temp_frame.grid_columnconfigure(5, minsize=each_column_width)
    temp_frame.grid_columnconfigure(6, minsize=each_column_width)

    if expiring_map_object:
        for key in list(expiring_map_object.dictionary.keys()):

            if key not in ignored_ip_set_object:
                packet_bean = expiring_map_object.get(key)

                def printOutPacketData(packet_bean):
                    if packet_bean:
                        populate_other_fields(packet_bean)

                        cell = tk.Label(temp_frame, text=packet_bean.communicatingIP)
                        cell.grid(row=row_index, column=0)

                        cell = tk.Label(temp_frame, text="protocol")
                        cell.grid(row=row_index, column=1)

                        cell = tk.Label(temp_frame, text=packet_bean.interface)
                        cell.grid(row=row_index, column=2)

                        cell = tk.Label(temp_frame, text=packet_bean.country)
                        cell.grid(row=row_index, column=3)

                        cell = tk.Label(temp_frame, text=packet_bean.state)
                        cell.grid(row=row_index, column=4)

                        cell = tk.Label(temp_frame, text=packet_bean.region)
                        cell.grid(row=row_index, column=5)

                        cell = tk.Label(temp_frame, text=packet_bean.domain_name)
                        cell.grid(row=row_index, column=6)

                printOutPacketData(packet_bean)
                row_index+=1

    temp_frame.pack()

    if should_listen_on_expiring_map_object:
        root.after(1000, response_object_reader)