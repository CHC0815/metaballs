import cv2

step = 10
level = 20
LINES = []


def scale(point):
    global step
    return (int(point[0] * step), int(point[1] * step))


def marching_squares(value_table, width, height):
    global LINES
    LINES = []
    for x in range(int(width/step) - 1):
        for y in range(int(height/step) - 1):
            state = get_state(
                value_table[x][y], value_table[x + 1][y], value_table[x + 1][y + 1], value_table[x][y + 1])
            a = scale((x + 0.5, y))
            b = scale((x + 1, y + 0.5))
            c = scale((x + 0.5, y + 1))
            d = scale((x, y + 0.5))
            if state == 1:
                LINES.append((c, d))
            elif state == 2:
                LINES.append((b, c))
            elif state == 3:
                LINES.append((b, d))
            elif state == 4:
                LINES.append((a, b))
            elif state == 5:
                LINES.append((a, d))
                LINES.append((b, c))
            elif state == 6:
                LINES.append((a, c))
            elif state == 7:
                LINES.append((a, d))
            elif state == 8:
                LINES.append((a, d))
            elif state == 9:
                LINES.append((a, c))
            elif state == 10:
                LINES.append((a, b))
                LINES.append((c, d))
            elif state == 11:
                LINES.append((a, b))
            elif state == 12:
                LINES.append((b, d))
            elif state == 13:
                LINES.append((b, c))
            elif state == 14:
                LINES.append((c, d))


def get_state(a, b, c, d):
    global level
    if a < level and b < level and c < level and d < level:
        return 0
    elif a < level and b < level and c < level and d >= level:
        return 1
    elif a < level and b < level and c >= level and d < level:
        return 2
    elif a < level and b < level and c >= level and d >= level:
        return 3
    elif a < level and b >= level and c < level and d < level:
        return 4
    elif a < level and b >= level and c < level and d >= level:
        return 5
    elif a < level and b >= level and c >= level and d < level:
        return 6
    elif a < level and b >= level and c >= level and d >= level:
        return 7
    elif a >= level and b < level and c < level and d < level:
        return 8
    elif a >= level and b < level and c < level and d >= level:
        return 9
    elif a >= level and b < level and c >= level and d < level:
        return 10
    elif a >= level and b < level and c >= level and d >= level:
        return 11
    elif a >= level and b >= level and c < level and d < level:
        return 12
    elif a >= level and b >= level and c < level and d >= level:
        return 13
    elif a >= level and b >= level and c >= level and d < level:
        return 14
    elif a >= level and b >= level and c >= level and d >= level:
        return 15


def main():
    global LINES
    source = cv2.VideoCapture(0)
    while True:

        ret, img = source.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        rows, cols = gray.shape
        marching_squares(gray, rows, cols)
        for line in LINES:
            gray = cv2.line(gray, line[0], line[1], (0, 0, 255), 1)
        cv2.imshow("Marching Squares", gray)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    source.release()


if __name__ == "__main__":
    main()
