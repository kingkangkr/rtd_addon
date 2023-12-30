from pynput import keyboard
import pyautogui
import datetime

def on_press(key):
    try:
        # Caps Lock 키가 눌렸을 때 스크린샷 찍기
        if key == keyboard.Key.caps_lock:
            # 현재 시간을 파일 이름으로 사용
            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png")
            pyautogui.screenshot(filename)
            print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Error: {e}")

# 키보드 리스너 시작
listener = keyboard.Listener(on_press=on_press)
listener.start()

# 리스너가 계속 실행되도록 유지 (실제 애플리케이션에서는 다른 방법을 사용할 수 있음)
listener.join()
