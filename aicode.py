import pygame
import numpy as np
import UI
import csv
import random
import os
import matplotlib.pyplot as plt  # Import even if not directly used here


# --- Helper Functions ---

def train_circle_size(shape, weights, bias, pixel_count, learning_rate, target_radius):
    """Trains the perceptron to recognize a specific circle size."""
    for x in range(pixel_count[0]):
        for y in range(pixel_count[1]):
            if shape[x, y]:
                # Adjust weight based on distance from center and target radius
                center_x = pixel_count[0] // 2
                center_y = pixel_count[1] // 2
                distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                # If the pixel is part of the circle, adjust weights based on how close it is to the target radius
                if abs(distance_from_center - target_radius) < 1:
                    weights[x, y] += learning_rate
                    bias[0] += learning_rate
                elif distance_from_center < target_radius:
                    weights[x,y] -= learning_rate * 0.5
                    bias[0] -= learning_rate * 0.5
                else:
                    weights[x,y] -= learning_rate * 0.5
                    bias[0] -= learning_rate * 0.5

def test(pixels, weights, bias, pixel_count):
    """Tests the perceptron's prediction for a given pixel pattern."""
    output = 0
    for x in range(pixel_count[0]):
        for y in range(pixel_count[1]):
            if pixels[x, y]:
                output += bias[0] + int(weights[x, y])
    print(f"Output: {output}")
    return output


def numpy_to_csv(array_2d, filename):
    """Saves a 2D NumPy array to a CSV file."""
    print("Saving...", end="\r")
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(array_2d)
        print("Saved.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def append_2d_list_to_csv(data_2d, filename, header=None):
    """Appends a 2D list to an existing CSV file."""
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if header and not file_exists:
            writer.writerow(header)
        writer.writerows(data_2d)


def csv_to_numpy(filename, pixel_count):
    """Loads a 2D NumPy array from a CSV file."""
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        if not rows:
            print("CSV file is empty or has incorrect")
            print("making a new array...")
            return np.zeros(pixel_count, dtype=np.int8)

        array_2d = np.array(rows, dtype=np.int8)

        if array_2d.shape != pixel_count:
            print(f"CSV file has incorrect shape: {array_2d.shape}, expected {pixel_count}")
            raise ValueError(f"Shape mismatch: Expected {pixel_count}, but got {array_2d.shape}")

        return array_2d

    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None


def sum_numpy_array(array_2d):
    """Sums all elements in a NumPy array."""
    if not isinstance(array_2d, np.ndarray):
        raise TypeError("Input must be a NumPy array.")
    if array_2d.size == 0:
        return 0
    return array_2d.sum().item()


def draw_circle_border_efficient(array, x, y, radius, thickness=1):
    """Draws a circle border on a NumPy array."""
    rows, cols = array.shape
    row_indices, col_indices = np.indices((rows, cols))
    distances = np.sqrt((row_indices - y)**2 + (col_indices - x)**2)
    border_indices = np.where(np.abs(distances - radius) < thickness)
    array[border_indices] = True
    return array


def atomic_trainings(weights, pixels, pixel_count, disable, bias, learning_rate, data_collection, target_radius):
    """Performs a single atomic training step."""
    print("Atomic training...")
    disable[0] = True

    # Determine the circle size (radius)
    shape = random.randint(0, 1)  # 0 for smaller, 1 for larger
    print("==> shape:", shape)
    pixels[:] = False  # Clear pixels before drawing

    if shape == 0:
        current_radius = target_radius - 2
    else:
        current_radius = target_radius + 2

    # Ensure the circle fits within the pixel grid
    loop = 0
    while True:
        loop += 1
        y = random.randint(current_radius, pixel_count[1] - current_radius - 1)
        x = random.randint(current_radius, pixel_count[0] - current_radius - 1)
        if loop > 200:
            print("!!!! Failed to find suitable shape.")
            return
        if (x - current_radius) >= 0 and (x + current_radius) < pixel_count[0] and (y - current_radius) >= 0 and (y + current_radius) < pixel_count[1]:
            break

    draw_circle_border_efficient(pixels, x, y, current_radius)

    prediction = test(pixels, weights, bias, pixel_count)
    error_rate = 0

    if shape == 1 and prediction < 0:
        train_circle_size(pixels, weights, bias, pixel_count, learning_rate, target_radius)
        print("==> train_circle_size (larger)")
        error_rate = prediction * -1
    elif shape == 0 and prediction >= 0:
        train_circle_size(pixels, weights, bias, pixel_count, learning_rate, target_radius)
        print("==> train_circle_size (smaller)")
        error_rate = prediction
    else:
        print("==> no training needed")

    print(f"==> shape: {shape}, prediction: {prediction}")
    data_collection.append([shape, shape == (prediction > 0), error_rate])

    disable[0] = False
    print("training Done")


# --- Main Function ---

def main():
    # --- Perceptron Setup ---
    pixel_size = 90
    hightmap_pixel_size = pixel_size // 3
    pixel_count = (10, 10)
    pixels = np.zeros(pixel_count, dtype=np.bool_)
    weights = csv_to_numpy("weights.csv", pixel_count)
    if weights is None:
        weights = np.zeros(pixel_count, dtype=np.int8)
    disable = [False]  # Changed to False initially

    # --- Data Collection ---
    data_collection = []

    bias = [0]
    learning_rate = 1
    target_radius = 3

    # --- Pygame Setup ---
    pygame.init()

    screen_width = pixel_count[0] * pixel_size + 220
    screen_height = pixel_count[1] * pixel_size + 5
    if pixel_count[0] * hightmap_pixel_size >= 200:
        screen_width = pixel_count[0] * pixel_size + 20 + (pixel_count[0] * hightmap_pixel_size)
        screen_height = 5 + pixel_count[1] * pixel_size
    screen = pygame.display.set_mode((screen_width, screen_height))

    screen.fill((50, 50, 95))
    clock = pygame.time.Clock()
    running = True

    # --- UI Elements ---
    button_width = 180
    button_height = 50
    button_x = pixel_count[0] * pixel_size + 10

    Train_larger_circle = UI.Button(screen, pygame.Rect(button_x, 10, button_width, button_height), "Train Larger", 30, (255, 255, 255), (80, 10, 10), (180, 80, 80), (255, 100, 100))
    Train_smaller_circle = UI.Button(screen, pygame.Rect(button_x, 70, button_width, button_height), "Train Smaller", 30, (255, 255, 255), (10, 80, 10), (80, 180, 80), (100, 255, 100))
    Test = UI.Button(screen, pygame.Rect(button_x, 200, button_width, button_height), "Test", 30, (255, 255, 255), (0, 0, 0), (80, 80, 80), (200, 200, 200))
    ato_train = UI.Button(screen, pygame.Rect(button_x, 130, button_width, button_height), "ato_train", 30, (255, 255, 255), (10, 10, 80), (80, 80, 180), (100, 100, 255))

    # --- Main Loop ---
    pressed = False
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Mouse Input ---
        if pygame.mouse.get_pressed(num_buttons=3)[0] != pressed:
            pressed = pygame.mouse.get_pressed(num_buttons=3)[0]

        if pressed:
            x, y = pygame.mouse.get_pos()
            try:
                pixels[x // pixel_size, y // pixel_size] = True
            except IndexError:
                pass

        if pygame.mouse.get_pressed(num_buttons=3)[1]:
            pixels[:] = False

        # --- Drawing ---
        screen.fill((50, 50, 95))

        for x in range(pixel_count[0]):
            for y in range(pixel_count[1]):
                pygame.draw.rect(surface=screen, color=(0, 0, 0) if pixels[x, y] else (255, 255, 255), rect=pygame.Rect((x * pixel_size, y * pixel_size, pixel_size, pixel_size)))

        # --- Hight Map ---
        for x in range(pixel_count[0]):
            for y in range(pixel_count[1]):
                color_value = 128 + int(weights[x, y])
                color = (color_value, 0, 255 - color_value)
                rect_x = (x * hightmap_pixel_size) + (pixel_size * pixel_count[0]) + 10
                rect_y = y * hightmap_pixel_size + ((pixel_size * pixel_count[1]) - (hightmap_pixel_size * pixel_count[1]))
                pygame.draw.rect(surface=screen, color=color, rect=pygame.Rect(rect_x, rect_y, hightmap_pixel_size, hightmap_pixel_size))

        # --- UI Updates ---
        Train_larger_circle.DrawAndUpdate(lambda: train_circle_size(pixels, weights, bias, pixel_count, learning_rate, target_radius + 2))
        Train_smaller_circle.DrawAndUpdate(lambda: train_circle_size(pixels, weights, bias, pixel_count, learning_rate, target_radius - 2))
        Test.DrawAndUpdate(lambda: test(pixels, weights, bias, pixel_count))
        if not disable[0]:
            ato_train.DrawAndUpdate(lambda: atomic_trainings(weights, pixels, pixel_count, disable, bias, learning_rate, data_collection, target_radius))

        # --- Atomic Training ---
        if not disable[0]:
            atomic_trainings(weights, pixels, pixel_count, disable, bias, learning_rate, data_collection, target_radius)

        # --- FPS and Screen Update ---
        fps = int(clock.get_fps())
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

    # --- Cleanup ---
    print(sum_numpy_array(weights))
    numpy_to_csv(weights, "weights.csv")
    append_2d_list_to_csv(data_collection, "data.csv", header=["Shape", "Correct", "Error"])
    pygame.quit()


if __name__ == "__main__":
    main()
