import tkinter
import math

##### 'CALCULATE' BUTTON #####

def calc_button_clicked():

    # Value for the radio button selection
    choice = selection.get()

    # Regardless of radio selection, convert the input to radius for all calculations
    # Use a string version of radius for text displays. Use a float version for calculations
    # Convert to absolute value in case user enters negative value
    
    # If Radius radio button selected:
    if choice == 1:
        rad_float = abs(float(radius_input.get().replace(',', '')))
    # If Diameter radio button selected:
    elif choice == 2:
        rad_float = abs(float(diameter_input.get().replace(',', '')) / 2)
    # If Circumference radio button selected:
    elif choice == 3:
        rad_float = abs(float(circumference_input.get().replace(',', '')) / (2 * math.pi))
    # If Area radio button selected:
    elif choice == 4:
        rad_float = math.sqrt(abs(float(area_input.get().replace(',', ''))) / math.pi)

    # String calculations for all parameters. Use radius to calculate all values. Set decimal precision
    # to whatever user specifies in input
    precision = decimal_input.get()
    radius_input.delete(0, 'end')
    radius_input.insert(0, f'{rad_float:,.{precision}f}')
    diameter_input.delete(0, 'end')
    diameter_input.insert(0, f'{rad_float * 2:,.{precision}f}')
    circumference_input.delete(0, 'end')
    circumference_input.insert(0, f'{2 * math.pi * rad_float:,.{precision}f}')
    area_input.delete(0, 'end')
    area_input.insert(0, f'{math.pi * rad_float * rad_float:,.{precision}f}')

    # Clear the canvas. This will allow for any previous circles to be removed.
    # Then redraw the axes and origin coordinates
    canvas.delete('all')
    draw_axes()

    # Set the radius string to match the radius float variable with decimal precision
    rad_str = f'{rad_float:,.{precision}f}'
    
    # If radius < 100 or > 300, call on draw_coords() function with current radius so grid coordinates can
    # adapt to the correct ratio, then set radius to min of 100 or max of 300 so that circle does not expand
    # beyond canvas boundary. Otherwise, use default radius
    if rad_float < 100 and rad_float != 0:
        draw_coords(rad_float)
        rad_float = 100
    elif rad_float > 300:
        draw_coords(rad_float)
        rad_float = 300
    else:
        draw_coords()

    # Draw the circle using rad_float as radius. rad_float must not be 0
    # Send circle to lowest layer of canvas so axes are visible over it
    if rad_float != 0:
        oval = canvas.create_oval(canvas_width / 2 - rad_float, canvas_height / 2 - rad_float, \
                                  canvas_width / 2 + rad_float, canvas_height / 2 + rad_float, \
                                  fill = 'lime green', outline = 'black')
        canvas.tag_lower(oval)
        
    # Draw the text for the x/y coordinates of perimeter tuples
    canvas.create_text(canvas_width / 2 + rad_float + 5, canvas_height / 2 + 10, \
                       anchor = tkinter.W, text = '(' + rad_str + ', 0)', fill = 'gray')
    canvas.create_text(canvas_width / 2 + 5, canvas_height / 2 - rad_float - 5, \
                       anchor = tkinter.SW, text = '(0, ' + rad_str + ')', fill = 'gray')

    canvas.pack()
    


##### 'CLEAR' BUTTON #####

def clear_button_clicked():

    # Clear all values. Re-draw axes and coordinates
    canvas.delete('all')
    selection.set(1)
    radius_input.delete(0, 'end')
    radius_input.insert(0, '0')
    diameter_input.delete(0, 'end')
    diameter_input.insert(0, '0')
    circumference_input.delete(0, 'end')
    circumference_input.insert(0, '0')
    area_input.delete(0, 'end')
    area_input.insert(0, '0')
    decimal_input.delete(0, 'end')
    decimal_input.insert(0, '2')
    draw_axes()
    draw_coords(100)



##### DRAW AXES, ORIGIN COORDINATES, GRIDLINE MARKERS #####

def draw_axes():
    
    # Draw axes and origin coordinates
    canvas.create_line(0, canvas_height / 2, canvas_width, canvas_height / 2, width = 1, fill='black')
    canvas.create_line(canvas_width / 2, 0, canvas_width / 2, canvas_height, width = 1, fill='black')
    canvas.create_text(canvas_width / 2 + 5, canvas_height / 2 + 10, anchor = tkinter.W, text = '(0, 0)')

    # Draw gridline markers
    x_gridlines = canvas_width / 8
    y_gridlines = canvas_height / 8
    for num in range(7):
        canvas.create_line(x_gridlines, canvas_height / 2 - 10, \
                           x_gridlines, canvas_height / 2 + 10, fill = 'black')
        canvas.create_line(canvas_width / 2 - 10, y_gridlines, \
                           canvas_width / 2 + 10, y_gridlines, fill = 'black')
        x_gridlines += canvas_width / 8
        y_gridlines += canvas_height / 8



##### DRAW GRID COORDINATES #####

def draw_coords(rad_float = 100):

    # If radius is <= 300, rightmost coordinate will be 3 * radius. Otherwise, coordinate will be
    # the current set radius. This will allow coordinates to adapt to radius size
    if rad_float <= 300:
        grid_val = rad_float * 3
    else:
        grid_val = rad_float

    # x/y coordinates will be set to increments that are 1/8 the size of the canvas
    grid_x_position = canvas_width - canvas_width / 8
    grid_y_position = 0 + canvas_height / 8

    # Set precision to current decimal input
    precision = decimal_input.get()
    
    # Run loop 7 times (skipping the middle coordinate), drawing the coordinates on screen. Then increment
    # the grid values accordingly 
    for num in range(7):
        if num != 3:
            canvas.create_text(grid_x_position, canvas_height / 2 + 20, text = f'{grid_val:,.{precision}f}')
            canvas.create_text(canvas_width / 2 + 35, grid_y_position, text = f'{grid_val:,.{precision}f}')
        grid_x_position -= canvas_width / 8
        grid_y_position += canvas_height / 8
        if rad_float <= 300:
            grid_val -= rad_float
        else:
            grid_val -= rad_float / 3



##### MAIN FUNCTION #####
            
# Create main window. Set to full screen
window = tkinter.Toplevel()
window.geometry('%dx%d' % (window.winfo_screenwidth(), window.winfo_screenheight()))

# Set canvas width/height constants
canvas_width = 800
canvas_height = 800

# Create top frame & canvas and bottom frame & button canvas
top_frame = tkinter.Frame(window, width = canvas_width, height = 1000)
top_frame.pack(side = 'top', pady = 10)
canvas = tkinter.Canvas(top_frame, width = canvas_width, height = canvas_height, bg = 'white', \
                        highlightbackground = 'black', highlightthickness = 1)
canvas.pack()
bottom_frame = tkinter.Frame(window, width = canvas_width, height = 100)
bottom_frame.pack(side = 'top', pady = 10)
bottom_frame.pack_propagate(0)
button_canvas = tkinter.Canvas(bottom_frame, width = canvas_width, height = 100, bg = 'lavender', \
                               highlightbackground = 'black', highlightthickness = 1)
button_canvas.pack()



##### RADIO BUTTONS #####

selection = tkinter.IntVar()
selection.set(1)

selection_radius = tkinter.Radiobutton(bottom_frame, text = 'Radius:', variable = selection, value = 1, bg = 'lavender')
selection_diameter = tkinter.Radiobutton(bottom_frame, text = 'Diameter:', variable = selection, value = 2, bg = 'lavender')
selection_circumference = tkinter.Radiobutton(bottom_frame, text = 'Circumference:', variable = selection, value = 3, bg = 'lavender')
selection_area = tkinter.Radiobutton(bottom_frame, text = 'Area:', variable = selection, value = 4, bg = 'lavender')

selection_radius.place(x = 200, y = 5)
selection_diameter.place(x = 200, y = 25)
selection_circumference.place(x = 200, y = 45)
selection_area.place(x = 200, y = 65)



##### USER INPUT AND BUTTONS #####

radius_input = tkinter.Entry(bottom_frame, width = 17, justify = 'right')
diameter_input = tkinter.Entry(bottom_frame, width = 17, justify = 'right')
circumference_input = tkinter.Entry(bottom_frame, width = 17, justify = 'right')
area_input = tkinter.Entry(bottom_frame, width = 17, justify = 'right')

# Insert a 0 in the user_input box. This will prevent error if user clicks 'Calculate' with a null value
radius_input.insert(0, '0')
diameter_input.insert(0, '0')
circumference_input.insert(0, '0')
area_input.insert(0, '0')

radius_input.place(x = canvas_width / 2 - 50, y = 10)
diameter_input.place(x = canvas_width / 2 - 50, y = 30)
circumference_input.place(x = canvas_width / 2 - 50, y = 50)
area_input.place(x = canvas_width / 2 - 50, y = 70)

# 'Calculate' button
calc_button = tkinter.Button(bottom_frame, text = 'Calculate', command = calc_button_clicked, height = 3, width = 8)
calc_button.place(x = canvas_width / 2 + 75, y = 20)

# 'Clear all' button
clear_button = tkinter.Button(bottom_frame, text = 'Clear all', command = clear_button_clicked, height = 3, width = 8)
clear_button.place(x = canvas_width / 2 + 150, y = 20)

# 'Back' button
back_button = tkinter.Button(bottom_frame, text = 'Back', command = lambda : window.destroy(), height = 3, width = 8)
back_button.place(x = 10, y = 20)

# Decimal precision input
decimal_label = tkinter.Label(bottom_frame, text = 'Dec. precision: ', bg = 'lavender')
decimal_label.place(x = canvas_width - 150, y = 10)
decimal_input = tkinter.Entry(bottom_frame, width = 5, justify = 'right')
decimal_input.insert(0, '2')
decimal_input.place(x = canvas_width - 50, y = 10)

# Draw default axes and default coordinates
draw_axes()
draw_coords(100)

# Run tkinter main loop
tkinter.mainloop()

