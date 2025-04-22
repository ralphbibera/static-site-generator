from generate_content import generate_pages_recursive
from copy_files import recursive_copy
import sys


def main():
    recursive_copy("./static", "./docs")
    base_path = "/" if len(sys.argv) == 1 else sys.argv[1]
    print(base_path)
    generate_pages_recursive("./content", "./template.html", "./docs", base_path)


if __name__ == "__main__":
    main()
