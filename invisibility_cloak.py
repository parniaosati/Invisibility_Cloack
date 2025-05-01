import cv2
import time
import numpy as np

# === States ===
ready_to_capture = False
background_captured = False
color_chosen = False
background = None
cloak_color = None
countdown_start_time = None
message_display_time = None
assistant_window_opened = False

# === UI Layout ===
button_ready = {"name": "READY", "top_left": (200, 180), "bottom_right": (400, 240)}
color_buttons = {
    'red': ((30, 120), (130, 170)), 'green': ((140, 120), (240, 170)), 'blue': ((250, 120), (350, 170)),
    'yellow': ((360, 120), (460, 170)), 'orange': ((470, 120), (570, 170)),
    'purple': ((30, 180), (130, 230)), 'brown': ((140, 180), (240, 230)),
    'gray': ((250, 180), (350, 230)), 'black': ((360, 180), (460, 230))
}

# === HSV Ranges ===
HSV_RANGES = {
    'red':    [(np.array([0, 110, 90]), np.array([10, 255, 255])), (np.array([170, 110, 90]), np.array([180, 255, 255]))],
    'green':  [(np.array([35, 70, 50]), np.array([85, 255, 255]))],
    'blue':   [(np.array([90, 70, 50]), np.array([130, 255, 255]))],
    'yellow': [(np.array([20, 100, 100]), np.array([35, 255, 255]))],
    'orange': [(np.array([10, 100, 100]), np.array([20, 255, 255]))],
    'purple': [(np.array([130, 60, 60]), np.array([160, 255, 255]))],
    'brown':  [(np.array([10, 100, 20]), np.array([20, 200, 200]))],
    'gray':   [(np.array([0, 0, 60]), np.array([180, 50, 200]))],
    'black':  [(np.array([0, 0, 0]), np.array([180, 255, 30]))]
}

# === Click Callback ===
def on_mouse(event, x, y, flags, param):
    global ready_to_capture, countdown_start_time, cloak_color, color_chosen
    if event == cv2.EVENT_LBUTTONDOWN:
        if not background_captured:
            x1, y1 = button_ready["top_left"]
            x2, y2 = button_ready["bottom_right"]
            if x1 <= x <= x2 and y1 <= y <= y2:
                ready_to_capture = True
                countdown_start_time = time.time()
        elif background_captured and not color_chosen:
            for color, (tl, br) in color_buttons.items():
                if tl[0] <= x <= br[0] and tl[1] <= y <= br[1]:
                    cloak_color = color
                    color_chosen = True
                    cv2.destroyWindow("Cloak Assistant")


def capture_background(cap):
    global background, background_captured, message_display_time
    for _ in range(30):
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            background = frame
            time.sleep(0.05)
    background_captured = True
    message_display_time = time.time()


def draw_assistant():
    canvas = np.ones((300, 600, 3), dtype=np.uint8) * 255  

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_small = 0.6
    font_large = 0.8

    if not background_captured:
        if not ready_to_capture:
            cv2.putText(canvas, "Step out of the frame!", (140, 40), font, font_large, (0, 0, 0), 2)

            x1, y1 = button_ready["top_left"]
            x2, y2 = button_ready["bottom_right"]
            cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 150, 0), -1)
            cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 100, 0), 3)

            text_size = cv2.getTextSize("READY", font, 1, 2)[0]
            text_x = x1 + (x2 - x1 - text_size[0]) // 2
            text_y = y1 + (y2 - y1 + text_size[1]) // 2
            cv2.putText(canvas, "READY", (text_x, text_y), font, 1, (255, 255, 255), 2)

        else:
            seconds = 3 - int(time.time() - countdown_start_time)
            if seconds > 0:
                cv2.putText(canvas, f"Capturing in {seconds}...", (170, 120), font, 1.2, (0, 0, 0), 3)
            else:
                cv2.putText(canvas, "Capturing background...", (140, 120), font, font_large, (0, 150, 0), 2)

    elif background_captured and not color_chosen:
        cv2.putText(canvas, "Choose your cloak color:", (150, 30), font, font_small, (50, 50, 50), 2)
        cv2.putText(canvas, "(Best: red, green, blue)", (180, 55), font, 0.5, (100, 100, 100), 1)

        for color, (tl, br) in color_buttons.items():
            color_bgr = {
                'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0),
                'yellow': (0, 255, 255), 'orange': (0, 165, 255), 'purple': (255, 0, 255),
                'brown': (42, 42, 165), 'gray': (128, 128, 128), 'black': (0, 0, 0)
            }.get(color, (255, 255, 255))

            text_color = (255, 255, 255) if np.mean(color_bgr) < 128 else (0, 0, 0)

            cv2.rectangle(canvas, tl, br, color_bgr, -1)
            cv2.rectangle(canvas, tl, br, (60, 60, 60), 2)

            text = color.upper()
            text_size = cv2.getTextSize(text, font, 0.5, 1)[0]
            text_x = tl[0] + (br[0] - tl[0] - text_size[0]) // 2
            text_y = tl[1] + (br[1] - tl[1] + text_size[1]) // 2
            cv2.putText(canvas, text, (text_x, text_y), font, 0.5, text_color, 1)

    return canvas

# === Main Loop ===
cap = cv2.VideoCapture(0)
cv2.namedWindow("Invisibility Cloak")

start_time = time.time()
assistant_delay = 2  # Seconds before assistant window opens

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    current_time = time.time()

    if not assistant_window_opened and current_time - start_time > assistant_delay:
        cv2.namedWindow("Cloak Assistant")
        cv2.setMouseCallback("Cloak Assistant", on_mouse)
        assistant_window_opened = True

    if ready_to_capture and not background_captured:
        if current_time - countdown_start_time >= 3:
            capture_background(cap)

    processed_frame = frame.copy()

    if background_captured and color_chosen:
        hsv = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2HSV)
        mask = sum(cv2.inRange(hsv, lower, upper) for lower, upper in HSV_RANGES[cloak_color])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
        inv_mask = cv2.bitwise_not(mask)
        cloak = cv2.bitwise_and(background, background, mask=mask)
        normal = cv2.bitwise_and(processed_frame, processed_frame, mask=inv_mask)
        processed_frame = cv2.add(cloak, normal)

    # === Show original feed in a small preview window ===
    original_preview = cv2.resize(frame, (320, 240))
    cv2.imshow("Original Preview", original_preview)

    # === Show processed output ===
    cv2.imshow("Invisibility Cloak", processed_frame)

    if assistant_window_opened and not (background_captured and color_chosen):
        assistant = draw_assistant()
        cv2.imshow("Cloak Assistant", assistant)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
