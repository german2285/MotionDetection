
![Kartynka](https://i.ibb.co/Pt63Hw7/9-Cu7i-KX2-I-4-2.jpg)
# MotionDetection
Детектор движения на видео

# Установка
Установите pip-пакеты с помощью команды:
```sh
$ pip install cv2
$ pip install os
```
---
## Настройка JSON файла
```json
"video_path": "input.mp4" Путь к видеофайлу, который будет обрабатываться. ВСЕГДА В .mp4
"output_directory": "output" Папка, в которой будут сохраняться кадры с обнаруженным движением.
"motion_threshold": 500 Пороговое значение, определяющее количество пикселей, которые должны измениться, чтобы считаться движущимся объектом. 
"delay_seconds": 1 Задержка в секундах между сохранением кадров с обнаруженным движением.
"square_size": 100 Размер квадратной области, которая будет выделена в центре видео. 
"window_width": 800 Ширина окна для отображения видео.
"window_height": 600 Высота окна для отображения видео.
```
## Управление 
Кнопки управления программой:

Кнопка "q": При нажатии на клавишу "q" программа завершается, и выполнение кода прекращается. Она используется для выхода из программы.
Кнопка "r": При нажатии на клавишу "r" происходит изменение размеров окна отображения видео. Она используется для изменения размеров окна приложения.
Перемещение квадратной области:

Квадратная область, выделенная в центре видео, может быть перетаскиваемой с помощью мыши.
Нажмите левую кнопку мыши на квадрате и перемещайте его в нужное место, удерживая кнопку.
Когда кнопка мыши отпущена, квадратная область перестанет перемещаться.

---

## FAQ 
Если потребители вашего кода часто задают одни и те же вопросы, добавьте ответы на них в этом разделе.

### Зачем вы разработали этот проект?
Для автограма и так далее

## To do
- [x] Добавить крутое README
- [ ] Сделать оптимизацию кадров
- [ ] ...

## Команда проекта
Оставьте пользователям контакты и инструкции, как связаться с командой разработки.

- [TREEWOOD](https://t.me/TREEWOOD2) — Junior developer

