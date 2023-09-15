from bezier_curve_approximation.GUI import ImageViewer
from tkinter import Tk

if __name__ == '__main__':
    root = Tk()
    root.configure(bg='white')
    root.title('Image Viewer')
    ImageViewer(root)
    root.resizable(0, 0)
    root.mainloop()

