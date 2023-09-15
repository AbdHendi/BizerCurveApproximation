from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import numpy as np
import time
from bezier_curve_approximation.optimization_algorithm import optimization
from utils.helper_function import plot_curves


coords = []
times = []
lines = []

c = []
t = []


#  Build A Image Viewer Now


class ImageViewer:

    def __init__(self, master):
        self.File = 'Capture.PNG'
        self.status = None
        self.master = master
        self.c_size = (800, 600)
        self.setup_gui(self.c_size)
        self.img = None
        self.master.bind('<space>', self.back)
        self.canvas.bind('<ButtonPress-1>', self.draw_line)
        self.canvas.bind('<ButtonRelease-1>', self.draw_line)

        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.reset_coords)

    def setup_gui(self, s):
        Label(self.master, text='Image Viewer', pady=5, bg='white', font=('Arial', 30)).pack()
        self.canvas = Canvas(self.master, height=s[1], width=s[0], bg='Black', bd=10, relief='ridge')
        self.canvas.old_coords = None
        self.canvas.pack()
        txt = '''
                                    Upload your Image
                                '''
        self.wt = self.canvas.create_text(s[0] / 2 - 270, s[1] / 2, text=txt, font=('', 30), fill='white')
        f = Frame(self.master, bg='white', padx=10, pady=10)
        Button(f, text='Open Image', bd=2, fg='white', bg='black', font=('', 15), command=self.make_image).pack(
            side=LEFT)
        Button(f, text='Start', bd=2, fg='white', bg='black', font=('', 15), command=self.save_result).pack(
            side=RIGHT)
        # Button(f, text='Exit', bd=2, fg='white', bg='black', font=('', 15), command=sys.exit).pack(
        # side=RIGHT)
        f.pack()

    def make_image(self):
        self.File = fd.askopenfilename()
        self.pilImage = Image.open(self.File)
        resized_img = self.pilImage.resize((700, 500), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resized_img)
        self.canvas.delete(ALL)
        self.canvas.create_image(60, 60, anchor=NW, image=self.img)
        # self.canvas.create_image(self.c_size[0] / 2 + 10, self.c_size[1] / 2 + 10, anchor=CENTER, image=self.img)

    def back(self, event):
        global coords, times
        coords = coords[:-50]
        times = times[:-50]
        for i in range(50):
            self.canvas.delete(lines.pop())
        print('update lines')
        return

    def draw(self, event):
        x, y = event.x, event.y
        if self.canvas.old_coords:
            x1, y1 = self.canvas.old_coords
            lines.append(self.canvas.create_line(x, y, x1, y1))
        self.canvas.old_coords = x, y
        c.append([x, y])
        t.append(int(time.time()))

    def draw_line(self, event):
        if str(event.type) == 'ButtonPress':
            self.canvas.old_coords = event.x, event.y

        elif str(event.type) == 'ButtonRelease':
            x, y = event.x, event.y
            x1, y1 = self.canvas.old_coords
            self.canvas.create_line(x, y, x1, y1, color='red')

    def reset_coords(self, event):
        global coords, times, c, t
        self.canvas.old_coords = None
        coords.append(c)
        times.append(t)
        c = []
        t = []

    def start_execution(self, connection_point_type='velocity'):
        start_exe = time.time()
        result_size = 0
        total_error = 0
        result_group = []
        im = Image.open(self.File)
        im = im.resize((700, 500), Image.ANTIALIAS)
        seq_size = 0
        for sub_coord, sub_time in zip(coords, times):
            points = np.array(sub_coord) - 60
            times_arr = np.array(sub_time)
            dx = []
            for i in range(1, len(points)):
                dx.append(np.linalg.norm(points[i] - points[i - 1]))
            dx = np.array(dx)
            dt = []
            for i in range(1, len(times_arr)):
                dt.append(times_arr[i] - times_arr[i - 1])

            velocity = (np.array(dx) / (np.array(dt) + 0.00001)).astype('int')
            inflection = np.where(velocity < 2)
            #np.save('points', points)
            #np.save('inflection', inflection)
            #points = np.load('points.npy')
            connection_points_indexes = inflection#np.load('inflection.npy')
            connection_points_indexes = connection_points_indexes[0].tolist()
            X_ = points[:, 0]
            Y_ = points[:, 1]
            sequence_points = np.array((X_, Y_)).T
            seq_size = len(sequence_points)
            # fixed-length connection points
            if connection_point_type == 'velocity':
                result, error, ioc = optimization(sequence_points, connection_points_indexes, 0.02, 0.7, 10000, im)
            else:
                result, error, ioc = optimization(sequence_points, None, 0.02, 0.7, 10000, im)

            result_group.append([result, sequence_points, 0.02, ioc, im])
            result_size += result.size * result.itemsize
            total_error += error / np.max(sequence_points)
        with open('performance.txt', 'a') as f:
            f.write('File name : result_{}  '.format(seq_size) + '\n')
            f.write('connection point method : {}'.format(connection_point_type) + '\n')
            f.write('Execution time ' + str(time.time() - start_exe) + ' sec' + '\n')
            f.write('Control points size in Byte : ' + str(result_size) + '\n')
            f.write('total error: ' + str(total_error) + '\n')
        for i, r in enumerate(result_group):
            if i == len(result_group) - 1:
                plot_curves(r[0], r[1], r[2], r[3], r[4], True, True, connection_point_type)
            else:
                plot_curves(r[0], r[1], r[2], r[3], r[4], True, False, connection_point_type)

    def save_result(self):
        self.start_execution()
        self.start_execution('fixed_length')



