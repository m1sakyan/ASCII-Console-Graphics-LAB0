import os
import sys
import time
import shutil
import msvcrt

# цвета ANSI
COLORS = [
    '\033[37m',  # белый
    '\033[32m',  # зеленый
    '\033[33m',  # желтый
    '\033[36m',  # голубой
    '\033[35m',  # пурпурный
]
RESET_COLOR = '\033[0m'


def get_terminal_size():
    size = shutil.get_terminal_size()
    return size.columns, size.lines


def clear_screen():
    os.system('cls')


def hide_cursor():
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write('\033[?25h')
    sys.stdout.flush()


def get_key():
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):
            key = msvcrt.getch()
            if key == b'K': return 'LEFT'
            if key == b'M': return 'RIGHT'
        elif key.lower() == b'q':
            return 'Q'
        elif key.lower() == b'c':
            return 'C'
    return None


def main():
    clear_screen()
    hide_cursor()

    text = " Computer Graphics ASCII Animation! "
    text_len = len(text)

    width, height = get_terminal_size()

    x_pos = 0
    direction = 1
    speed = 0.05
    color_idx = 0

    y_pos = height // 2

    sys.stdout.write(f"\033[{height};1H")
    sys.stdout.write("Стрелки: направление | C: цвет | Q: выход | Текущий цвет: 1")
    sys.stdout.flush()

    try:
        while True:
            key = get_key()
            if key == 'Q':
                break
            elif key == 'LEFT':
                direction = -1
            elif key == 'RIGHT':
                direction = 1
            elif key == 'C':
                color_idx = (color_idx + 1) % len(COLORS)

                sys.stdout.write(f"\033[{height};1H")
                sys.stdout.write(f"Стрелки: направление | C: цвет | Q: выход | Текущий цвет: {color_idx + 1}")
                sys.stdout.flush()

            new_width, new_height = get_terminal_size()
            if new_width != width or new_height != height:
                width, height = new_width, new_height
                y_pos = height // 2
                clear_screen()
                sys.stdout.write(f"\033[{height};1H")
                sys.stdout.write(f"Стрелки: направление | C: цвет | Q: выход | Текущий цвет: {color_idx + 1}")
                sys.stdout.flush()

            if direction == 1 and x_pos > width:
                x_pos = -text_len
            elif direction == -1 and x_pos < -text_len:
                x_pos = width

            start_x = max(0, x_pos)
            end_x = min(width, x_pos + text_len)

            sys.stdout.write(f"\033[{y_pos};1H")
            sys.stdout.write('\033[K')

            if start_x < end_x:
                text_start = start_x - x_pos
                text_end = end_x - x_pos
                visible_text = text[text_start:text_end]

                if start_x > 0:
                    sys.stdout.write(f"\033[{start_x}C")

                sys.stdout.write(COLORS[color_idx] + visible_text + RESET_COLOR)

            sys.stdout.flush()

            x_pos += direction

            time.sleep(speed)

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(RESET_COLOR)
        show_cursor()

        sys.stdout.write(f"\033[{height};1H\n")
        print("Программа завершена. Цвета восстановлены.")


if __name__ == "__main__":
    main()