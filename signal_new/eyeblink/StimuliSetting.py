import json
import math


def main():
    d = {
        'a': (8.0, 0.0),
        'b': (8.3, 0.35 * math.pi),
        'c': (8.6, 0.70 * math.pi),
        'd': (8.9, 1.05 * math.pi),
        'e': (9.2, 1.40 * math.pi),
        'f': (9.5, 1.75 * math.pi),
        'g': (9.8, 0.10 * math.pi),
        'h': (10.1, 0.45 * math.pi),
        'i': (10.4, 0.80 * math.pi),
        'j': (10.7, 1.15 * math.pi),
        'k': (11.0, 1.50 * math.pi),
        'l': (11.3, 1.85 * math.pi),
        'm': (11.6, 0.20 * math.pi),
        'n': (11.9, 0.55 * math.pi),
        'o': (12.2, 0.90 * math.pi),
        'p': (12.5, 1.25 * math.pi),
        'q': (12.8, 1.60 * math.pi),
        'r': (13.1, 1.95 * math.pi),
        's': (13.4, 0.30 * math.pi),
        't': (13.7, 0.65 * math.pi),
        'u': (14.0, 1.00 * math.pi),
        'v': (14.3, 1.35 * math.pi),
        'w': (14.6, 1.70 * math.pi),
        'x': (14.9, 0.05 * math.pi),
        'y': (15.2, 0.40 * math.pi),
        'z': (15.5, 0.75 * math.pi),
        ' ': (15.8, 1.10 * math.pi)
    }

    with open('stimuli.json', 'w') as fp:
        json.dump(d, fp)


if __name__ == '__main__':
    main()
