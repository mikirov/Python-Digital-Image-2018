import getopt
import sys

from visualizer import Visualizer


def main(argv):
    url = None
    try:
        opts, args = getopt.getopt(argv, "u:", ["url="])
    except getopt.GetoptError:
        print("main.py -u <url>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("u", "--url"):
            url = arg

    if url is None:
        url = "https://backend.deviantart.com/rss.xml?q=special%3Add"
    print(f"url is {url}")
    visualiser = Visualizer(url)
    visualiser.run()


if __name__ == "__main__":
    main(sys.argv[1:])
