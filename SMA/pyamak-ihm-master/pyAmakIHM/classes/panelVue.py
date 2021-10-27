"""
Class PanelVue
"""

from tkinter import Canvas, Frame, PhotoImage, Toplevel

class PanelVue(Canvas):
    """
    Class PanelVue
    """

    def __init__(
            self,
            root : 'Tk'
    ) -> None :

        super().__init__(root,bg='white')

        self.__root = root

        self.pack(fill='both',expand='yes')
        self.configure(scrollregion=(0,0,250,150))

        self.bind("<ButtonPress-1>", self.scroll_start)
        self.bind("<B1-Motion>", self.scroll_move)
        self.pack(fill='both',side='right',expand='yes')

        self.__images = []

    def get_canvas_width(self) -> float:
        self.__root.update()
        return self.winfo_width()

    def get_canvas_height(self) -> float:
        self.__root.update()
        return self.winfo_height()

    """
    Link to the mouse button to navigate in the canvas
    """
    def scroll_start(self, event) -> None:
        self.scan_mark(event.x, event.y)

    """
    Link to the mouse movement to navigate in the canvas
    """
    def scroll_move(self, event) -> None:
        self.scan_dragto(event.x, event.y, gain=1)

    """
    Draw a rectangle with x,y coords, height, width and color
    """
    def draw_rectangle(self, x : float, y : float, height : float, width : float, color : str) -> int:
        return self.create_rectangle(
            x-width/2,
            y-height/2,
            x+width/2,
            y+height/2,
            fill=color)

    """
    Draw a circle with x,y coords, radian and color
    """
    def draw_circle(self, x : float, y : float, radian : float, color : str) -> int:
        return self.create_oval(
            x-radian,
            y-radian,
            x+radian,
            y+radian,
            fill=color)

    """
    Draw a line between x0,y0 and x1,y1 point with color
    """
    def draw_line(self, x0 : float, y0 : float, x1 : float, y1 : float, color : str) -> int:
        return self.create_line(x0,y0,x1,y1,fill=color)

    """
    Draw an image with x,y coords and its name
    """
    def draw_image(self, x : float, y : float, name : str) -> int:

        new = True
        for img in self.__images:
            if(img.cget('file') == name):
                new = False
                new_image = img

        if(new):
            new_image = PhotoImage(file=name)
            self.__images.append(new_image)

        return self.create_image(x,y,image=new_image)

    """
    Draw a text with x,y coords
    """
    def draw_text(self, x : float, y : float, text : str) -> int:
        return self.create_text(x,y,anchor="w",fill='black',text=text)

    """
    Move an element to x,y coords
    """
    def move_element(self, element : int, x : float, y : float) -> None:
        coords = self.coords(element)
        width = coords[2] - coords[0]
        height = coords[3] - coords[1]
        self.coords(
            element,
            x-width/2,
            y-height/2,
            x+width/2,
            y+height/2)

    """
    Remove an element
    """
    def remove_element(self, element : int) -> None:
        self.delete(element)

    """
    Remove all element
    """
    def remove_all(self) -> None:
        self.delete('all')

    """
    Give the element's coords
    """
    def get_coords_element(self, element : int) -> (float,float):
        coords = self.coords(element)
        return(coords[0] + (coords[2] - coords[0]) / 2, coords[1] + (coords[3] - coords[1]) / 2)

    """
    Give the image's coords
    """
    def get_coords_image(self, image : int) -> (float,float):
        return self.coords(image)

    """
    Move an image to x,y coords
    """
    def move_image(self, image : int, x : float, y : float) -> None:
        self.coords(image,x,y)

    """
    Change the color of the element
    """
    def change_color(self, element : int, color : str) -> None:
        self.itemconfig(element,fill=color)
