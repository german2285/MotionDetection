import cv2
import time
import os
import platform
import json

def load_variables_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    video_path = data["video_path"]
    output_directory = data["output_directory"]
    motion_threshold = data["motion_threshold"]
    delay_seconds = data["delay_seconds"]
    square_size = data["square_size"]
    window_width = data["window_width"]
    window_height = data["window_height"]

    return video_path, output_directory, motion_threshold, delay_seconds, square_size, window_width, window_height



json_file_path = "config.json"


video_path, output_directory, motion_threshold, delay_seconds, square_size, window_width, window_height = load_variables_from_json(
    json_file_path)


os.makedirs(output_directory, exist_ok=True)


video_capture = cv2.VideoCapture(video_path)


if not video_capture.isOpened():
    print("Не удалось открыть видео.")
    exit()


ret, frame = video_capture.read()


if not ret:
    print("Не удалось прочитать первый кадр видео.")
    exit()


height, width, _ = frame.shape


square_x = (width - square_size) // 2
square_y = (height - square_size) // 2


dragging = False


prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
motion_detected = False
last_motion_time = time.time()



def mouse_callback(event, x, y, flags, param):
    global square_x, square_y, dragging

    if event == cv2.EVENT_LBUTTONDOWN:
        
        if square_x <= x < square_x + square_size and square_y <= y < square_y + square_size:
            dragging = True

    elif event == cv2.EVENT_LBUTTONUP:
        
        dragging = False

    elif event == cv2.EVENT_MOUSEMOVE:
        
        if dragging:
            square_x = x - square_size // 2
            square_y = y - square_size // 2


# Создаем окно для отображения видео
window_name = "Video"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_name, mouse_callback)

# Читаем видео кадр за кадром
while True:
    # Читаем текущий кадр
    ret, frame = video_capture.read()

    # Если кадр не удалось прочитать, выходим из цикла
    if not ret:
        break

   
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Вычисляем разницу между текущим и предыдущим кадром
    frame_delta = cv2.absdiff(prev_frame, gray_frame)

    # Применяем пороговое значение для выделения движущихся объектов
    thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]

    
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, None)

    # Выделяем квадратную область в центре видео
    region_of_interest = thresh[square_y:square_y + square_size, square_x:square_x + square_size]

    # Проверяем, обнаружено ли движение внутри квадратной области
    if cv2.countNonZero(region_of_interest) > motion_threshold:
        current_time = time.time()
        if current_time - last_motion_time >= delay_seconds:
            frame_name = os.path.join(output_directory, f"frame_{current_time}.jpg")
            cv2.imwrite(frame_name, frame)
            last_motion_time = current_time

    
    prev_frame = gray_frame.copy()

    # Отображаем текущий кадр с выделенной областью
    cv2.rectangle(frame, (square_x, square_y), (square_x + square_size, square_y + square_size), (0, 255, 0), 2)
    cv2.imshow(window_name, frame)

    # Ждем нажатия клавиши и проверяем, нужно ли изменить размеры окна
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("r"):
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, window_width, window_height)


video_capture.release()
cv2.destroyAllWindows()

# Открываем папку output
if platform.system() == "Windows":
    os.startfile(output_directory)
elif platform.system() == "Darwin":
    subprocess.Popen(["open", output_directory])
elif platform.system() == "Linux":
    subprocess.Popen(["xdg-open", output_directory])
