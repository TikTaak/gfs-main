from src.main import Main
from src.server import Server

if __name__ == '__main__':
    main = Main()
    main.do_progress()
    server = Server(main)