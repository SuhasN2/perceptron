import pygame, numpy, UI, csv, random,os
import matplotlib.pyplot as plt


# functions
def train_shape_1(shape,weights,bias,pixel_count,learning_rate):
    for x in range(pixel_count[0]):
        for y in range(pixel_count[1]):
            if shape[x, y] == 1:
                weights[x, y] += learning_rate
                bias[0] += learning_rate


def train_shape_2(shape,weights,bias,pixel_count,learning_rate):
    for x in range(pixel_count[0]):
        for y in range(pixel_count[1]):
            if shape[x, y] == 1:
                weights[x, y] -= learning_rate
                bias[0] -= learning_rate


def test(pixels, weights, bias, pixel_count):
    output = 0
    for x in range(pixel_count[0]):
        for y in range(pixel_count[1]):
            if pixels[x, y] == 1:
                output +=  bias[0] + int(weights[x, y])
    
    print(f"Output: {output}") # todo: implement output on gui output
    return output

def numpy_to_csv(array_2d, filename):
    """Saves a 2D NumPy array to a CSV file.

    Args:
        array_2d: The 2D NumPy array.
        filename: The name of the CSV file.
    """
    print("Saving...", end="\r")
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(array_2d)  # Efficiently write all rows
            print("Saved.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def append_2d_list_to_csv(data_2d, filename, header=None):#! ?
    """Appends a 2D list to an existing CSV file.

    Args:
        data_2d: The 2D list (list of lists) to append.
        filename: The name of the CSV file.
        header: (Optional) A list of strings representing the column headers.
                If provided and the file doesn't exist, the header will be 
                written. If the file exists, the header is ignored.
    """

    file_exists = os.path.isfile(filename)  # Check if the file exists
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:  # 'a' for append mode
        writer = csv.writer(csvfile)

        if header and not file_exists:  # Write header only if file doesn't exist
            writer.writerow(header)
        writer.writerows(data_2d)


def csv_to_numpy(filename,pixel_count):

    try:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)  # Read all rows into a list

                # Check if the CSV is empty or has inconsistent row lengths
        if not rows:
            print("CSV file is empty or has incorrect")
            print("making a new array...")
            return numpy.zeros(pixel_count, dtype=numpy.int8)

        array_2d = numpy.array(rows, dtype=numpy.int8)

        if array_2d.shape!= pixel_count:
            print(f"CSV file has incorrect shape: {array_2d.shape}, expected {pixel_count}")
            raise  ValueError(f"Shape mismatch: Expected {pixel_count}, but got {array_2d.shape}")



        # Check if the array has the correct data

        
        return array_2d

    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None

def sum_numpy_array(array_2d):# ?
    """Adds every single value in a NumPy array, returning a standard Python number.

    Args:
        array_2d: The NumPy array (can be any dimension).

    Returns:
        The sum of all elements in the array as a standard Python number (int or float).
        Returns 0 if the inumpyut array is empty.
        Raises TypeError if the inumpyut is not a numpy array.
    """

    if not isinstance(array_2d, numpy.ndarray):
        raise TypeError("Inumpyut must be a NumPy array.")

    if array_2d.size == 0:  # Check if the array is empty
        return 0

    return array_2d.sum().item()  # Use .item() to extract the Python number

def draw_circle_border_efficient(array, x, y, radius, thickness=1):  # Added thickness parameter
    rows, cols = array.shape
    row_indices, col_indices = numpy.indices((rows, cols))
    distances = numpy.sqrt((row_indices - y)**2 + (col_indices - x)**2)

    # Use numpy.where for efficiency
    border_indices = numpy.where(numpy.abs(distances - radius) < thickness)
    array[border_indices] = True
    return array


def atomic_trainings(weights,pixels,pixel_count,disable,bias,learning_rate,data_collection):
    print("Atomic training...")
    disable[0] = True

    # chick for collegian 
    size = random.randint(0,1)
    print("==> size:",size)

    if size == 0:
        find_circle(pixels,pixel_count,radius_size=1)
        
    else:
        find_circle(pixels,pixel_count,radius_size=2)
      
    prediction = test(pixels,weights,bias,pixel_count)
    error_rate = 0

    if size == True and prediction < 0:
        train_shape_1(pixels, weights, bias, pixel_count, learning_rate)
        print("==> train_size_1")
        error_rate = prediction * -1
    elif size == False and prediction >= 0:
        train_shape_2(pixels, weights, bias, pixel_count, learning_rate)
        print("==> train_size_2")
        error_rate = prediction 
    else:
        print("==> no training needed")

    pixels[:] = False
    print(f"==> shape: {size}, prediction: {prediction}")



    data_collection.append([size == True,size == (prediction > 0),error_rate])

    disable[0] = False
    print (f"training Done")


def find_circle(pixels,pixel_count,radius_size=1):
    loop = 0
    while True:
        loop += 1
        y = random.randint(0,pixel_count[1])

        if radius_size == 1:
            x = random.randint(pixel_count[0]/2+3,pixel_count[0])
        else:
            x = random.randint(0,pixel_count[0]/2-3)
            

        # circle
        if pixel_count[0] < pixel_count[1]:
            radius = random.randint(int(pixel_count[0]),(pixel_count[0]))
        else:
            radius = random.randint(int(pixel_count[1]),(pixel_count[1]))
            # radius -= 1
        
        # diameter = radius * 2

        # check for collisions
        # if (x - radius) + diameter < pixel_count[0] or (y - radius) + diameter < pixel_count[1]:
            # break

        if loop > 200:
            print("!!!! 2 Failed to find suitable shape.")
            break

        draw_circle_border_efficient(pixels,x,y,radius)

def main():
    # perception setup
    pixel_size = 80
    hightmap_pixel_size = pixel_size//3
    pixel_count = (24,24)
    pixels = numpy.zeros(pixel_count, dtype=numpy.bool) # numpy array for the pixels
    weights = csv_to_numpy("weights.csv",pixel_count)
    disable = [True]

    # data collection
    data_collection = []

    bias = [0]# bias
    learning_rate = 1 # learning rate

    # pygame setup
    pygame.init()

    if pixel_count[0] *  hightmap_pixel_size < 200:
        screen = pygame.display.set_mode((pixel_count[0]*pixel_size + 220, pixel_count[1]*pixel_size + 5))
    else:
        screen = pygame.display.set_mode((pixel_count[0]*pixel_size + 20 + (pixel_count[0] * hightmap_pixel_size ),5 + pixel_count[1]*pixel_size))
    
    screen.fill((50, 50, 95))
    clock = pygame.time.Clock()
    running = True

    # create buttons
    Train_big_shape = UI.Button(screen, pygame.Rect(pixel_count[0]*pixel_size + 10, 10, 180, 50,), "Train 1", 30, (255, 255, 255), (80, 10, 10), (180, 80, 80), (255, 100, 100))
    draw_big_circle = UI.Button(screen, pygame.Rect(pixel_count[0]*pixel_size + 15, 10, 180, 50,), "Train 1", 30, (255, 255, 255), (80, 10, 10), (180, 80, 80), (255, 100, 100))
    Train_small_shape = UI.Button(screen, pygame.Rect(pixel_count[0]*pixel_size + 10, 70, 180, 50,), "Train 2", 30, (255, 255, 255), (10, 80, 10), (80, 180, 80), (100, 255, 100))
    draw_small_circle = UI.Button(screen, pygame.Rect(pixel_count[0]*pixel_size + 10, 70, 180, 50,), "Train 2", 30, (255, 255, 255), (10, 80, 10), (80, 180, 80), (100, 255, 100))
    Test = UI.Button(screen, pygame.Rect(pixel_count[0]*pixel_size + 10, 200, 180, 50,), "Test", 30, (255, 255, 255), (0, 0, 0), (80, 80, 80), (200, 200, 200))
    ato_train = UI.Button(screen, pygame.Rect(pixel_count[0]*pixel_size + 10, 130, 180, 50,), "ato_train", 30, (255, 255, 255), (10, 10, 80), (80, 80, 180), (100, 100, 255))
    
    # todo select_model = UI.Dropdown(screen, pygame.Rect(pixel_count[0]*pixel_size + 10, 250, 180, 50,),["cat","dog","elephant"] ,30 ,(255, 255, 255), (80, 10, 10), (180, 80, 80), (255, 100, 100))
    # todo toggle_button = UI.Toggle(screen=screen,rect = pygame.Rect(pixel_count[0]*pixel_size + 10,(hightmap_pixel_size + ((pixel_size * pixel_count[1]) - (hightmap_pixel_size * pixel_count[1]))) - 60,180,50),text="Feature",font_size=24,font_color=(255, 255, 255),bg_color=(220, 220, 220),hover_bg_color=(200, 200, 200),click_bg_color=(105, 105, 105),checked_bg_color=(0, 255, 0))
    
    # main loop
    pressed = False

    while running:
        # mouse click event
        if pygame.mouse.get_pressed(num_buttons=3)[0] != pressed:
            pressed = pygame.mouse.get_pressed(num_buttons=3)[0]
            
        if pressed:
            x, y = pygame.mouse.get_pos()
            
            try:
                pixels[x//pixel_size, y//pixel_size] = True # todo implement the line drawing algorithm
            except IndexError: pass 

        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pixels[:] = False
                    print("pixels cleared")
        

        # clear pixels
        if pygame.mouse.get_pressed(num_buttons=3)[1] == True:
            pixels[:] = False
            print("pixels cleared")
            
        # draw pixels
        for x in range(pixel_count[0]):
            for y in range(pixel_count[1]):
                pygame.draw.rect(surface=screen, color=(0,0,0) if pixels[x, y] else (255,255,255), rect=pygame.Rect((x*pixel_size, y*pixel_size, pixel_size, pixel_size)))

        # draw hight map 

        for x in range(pixel_count[0]):
            for y in range(pixel_count[1]):
                pygame.draw.rect(surface=screen, color=((128 + int(weights[x, y]),0,(255 - (128 + int(weights[x, y]))))), rect=pygame.Rect(((x*hightmap_pixel_size) + (pixel_size * pixel_count[0]) + 10, y * hightmap_pixel_size + ((pixel_size * pixel_count[1])- (hightmap_pixel_size * pixel_count[1])), hightmap_pixel_size, hightmap_pixel_size)))

        # update Button
        Train_big_shape.DrawAndUpdate(lambda:train_shape_1(pixels,weights,bias,pixel_count,learning_rate))
        draw_big_circle.DrawAndUpdate()
        Train_small_shape.DrawAndUpdate(lambda:train_shape_2(pixels,weights,bias,pixel_count,learning_rate))
        draw_small_circle.DrawAndUpdate()
        Test.DrawAndUpdate(lambda:test(pixels,weights,bias,pixel_count))
        # todo select_model.DrawAndUpdate()
        # todo toggle_button.DrawAndUpdate()
        ato_train.DrawAndUpdate(lambda:atomic_trainings(weights,pixels,pixel_count,disable,bias,learning_rate,data_collection))
        atomic_trainings(weights,pixels,pixel_count,disable,bias,learning_rate,data_collection)

        #calculate FPS
        fps = int(clock.get_fps())
        # print(f"\rfps ={fps}\r",end="")
        # update screen
        pygame.display.update()
        pygame.display.flip()
        
        clock.tick(60)  # limits FPS to 60
        screen.fill((50, 50, 95))

    print(sum_numpy_array(weights))
    # save weights to csv file
    numpy_to_csv(weights,"weights.csv")
    append_2d_list_to_csv(data_collection,"data.csv")
    pygame.quit()

if __name__ == "__main__":
    main()