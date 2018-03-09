from __future__ import division
from tkinter import *
from PIL import ImageTk, Image

APP_NAME = "CZ4071 graph visualization"

def display_image(widget, image_file, width, height):
    """
    Put image into canvas
    """
    #img_ori = Image.open("tpch_graph.png")
    #img_ori = img_ori.resize(, Image.ANTIALIAS)
    #img = ImageTk.PhotoImage(img_ori)
    #graph_canvas = Label(graph_region, image=img, width=graph_width, height=graph_height)
    #graph_canvas.pack()

if __name__ == "__main__":
    # the app window
    root = Tk()
    root.title(APP_NAME)
    screen_width = root.winfo_screenwidth() - 50
    screen_height = root.winfo_screenheight() - 100
    root.geometry(str(screen_width) + "x" + str(screen_height))
    root.resizable(width=False, height=False)

    # the graph visualization region
    graph_width = int(screen_width * 0.73)
    graph_height = screen_height - 60
    graph_region = Frame(root, width=graph_width, height=graph_height)
    graph_region.grid(row=0, rowspan=3, column=0)
    Label(graph_region, text="Graph").pack()
    img_ori = Image.open("tpch_graph.png")
    img_ori = img_ori.resize((graph_width, graph_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img_ori)
    graph_canvas = Label(graph_region, image=img, width=graph_width, height=graph_height)
    graph_canvas.pack()

    # the plot region
    plot_width = screen_width - graph_width
    plot_height = int(graph_height / 3) - 20

    # plot for TPC-H graph
    plot_region1 = Frame(root, width=plot_width, height=plot_height)
    plot_region1.grid(row=0, column=1)
    Label(plot_region1, text="TPC-H graph property").pack()
    img_ori2 = Image.open("tpch_graph.png")
    img_ori2 = img_ori2.resize((plot_width, plot_height), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img_ori2)
    plot_canvas1 = Label(plot_region1, image=img2, width=plot_width, height=plot_height)
    plot_canvas1.pack()

    # plot for random graph
    plot_region2 = Frame(root, width=plot_width, height=plot_height)
    plot_region2.grid(row=1, column=1)
    Label(plot_region2, text="Random graph property").pack()
    img_ori3 = Image.open("tpch_graph.png")
    img_ori3 = img_ori3.resize((plot_width, plot_height), Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(img_ori3)
    plot_canvas2 = Label(plot_region2, image=img3, width=plot_width, height=plot_height)
    plot_canvas2.pack()

    # plot for scale-free graph
    plot_region3 = Frame(root, width=plot_width, height=plot_height)
    plot_region3.grid(row=2, column=1)
    Label(plot_region3, text="Scale-free graph property").pack()
    img_ori4 = Image.open("tpch_graph.png")
    img_ori4 = img_ori4.resize((plot_width, plot_height), Image.ANTIALIAS)
    img4 = ImageTk.PhotoImage(img_ori4)
    plot_canvas3 = Label(plot_region3, image=img4, width=plot_width, height=plot_height)
    plot_canvas3.pack()

    # button region
    button_region = Frame(root, width=screen_width, height=60)
    button_region.grid(row=3, column=0, columnspan=2)
    Label(button_region, text="Choose graph:").pack(side=LEFT)
    Button(button_region, text="TPC-H").pack(side=LEFT)
    Button(button_region, text="Random").pack(side=LEFT)
    Button(button_region, text="Scale-free").pack(side=LEFT)
    Label(button_region, text="Choose property:").pack(side=LEFT)
    Button(button_region, text="Betweenness").pack(side=LEFT)
    Button(button_region, text="Closeness").pack(side=LEFT)
    Button(button_region, text="Degree distribution").pack(side=LEFT)
    Button(button_region, text="Betweenness").pack(side=LEFT)
    Button(button_region, text="Betweenness").pack(side=LEFT)
    Button(button_region, text="Betweenness").pack(side=LEFT)

    root.mainloop()
