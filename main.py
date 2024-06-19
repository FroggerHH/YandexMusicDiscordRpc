import session
import atexit
atexit.register(session.shutdown)

# Запуск
if __name__ == "__main__":
    session.startup(None)