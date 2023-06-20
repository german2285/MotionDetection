import cv2
import time
import os
import platform
import json


# Загрузка переменных из файла JSON
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


# Указать путь к файлу JSON с переменными
json_file_path = "config.json"

# Загрузить переменные из файла JSON
video_path, output_directory, motion_threshold, delay_seconds, square_size, window_width, window_height = load_variables_from_json(
    json_file_path)

# Создаем папку для сохранения кадров
os.makedirs(output_directory, exist_ok=True)

# Инициализируем видеозахват
video_capture = cv2.VideoCapture(video_path)

# Проверяем, удалось ли открыть видео
if not video_capture.isOpened():
    print("Не удалось открыть видео.")
    exit()

# Читаем первый кадр видео
ret, frame = video_capture.read()

# Проверяем, удалось ли прочитать первый кадр
if not ret:
    print("Не удалось прочитать первый кадр видео.")
    exit()

# Получаем размеры видео
height, width, _ = frame.shape

# Определяем начальные координаты квадратной области в центре видео
square_x = (width - square_size) // 2
square_y = (height - square_size) // 2

# Переменная для отслеживания перетаскивания квадрата
dragging = False

# Инициализируем переменные
prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
motion_detected = False
last_motion_time = time.time()


# Функция обработки событий мыши
def mouse_callback(event, x, y, flags, param):
    global square_x, square_y, dragging

    if event == cv2.EVENT_LBUTTONDOWN:
        # При нажатии кнопки мыши начинаем перетаскивание квадрата
        if square_x <= x < square_x + square_size and square_y <= y < square_y + square_size:
            dragging = True

    elif event == cv2.EVENT_LBUTTONUP:
        # При отпускании кнопки мыши завершаем перетаскивание квадрата
        dragging = False

    elif event == cv2.EVENT_MOUSEMOVE:
        # При перемещении мыши обновляем координаты квадрата, если происходит перетаскивание
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

    # Преобразуем текущий кадр в градации серого
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Вычисляем разницу между текущим и предыдущим кадром
    frame_delta = cv2.absdiff(prev_frame, gray_frame)

    # Применяем пороговое значение для выделения движущихся объектов
    thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]

    # Удаляем шум с помощью морфологической операции "открытие"
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, None)

    # Выделяем квадратную область в центре видео
    region_of_interest = thresh[square_y:square_y + square_size, square_x:square_x + square_size]

    # Проверяем, обнаружено ли движение внутри квадратной области
    if cv2.countNonZero(region_of_interest) > motion_threshold:
        # Обнаружено движение, сохраняем кадр, если прошло достаточно времени с момента последнего сохранения
        current_time = time.time()
        if current_time - last_motion_time >= delay_seconds:
            frame_name = os.path.join(output_directory, f"frame_{current_time}.jpg")
            cv2.imwrite(frame_name, frame)
            last_motion_time = current_time

    # Обновляем предыдущий кадр
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

# Освобождаем ресурсы
video_capture.release()
cv2.destroyAllWindows()

# Открываем папку output после завершения программы
if platform.system() == "Windows":
    os.startfile(output_directory)
elif platform.system() == "Darwin":
    subprocess.Popen(["open", output_directory])
elif platform.system() == "Linux":
    subprocess.Popen(["xdg-open", output_directory])