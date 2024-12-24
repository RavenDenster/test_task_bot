from functools import wraps
import time

def retry_decorator(attempts, delay, exceptions=None):
    """
    Декоратор для повторного выполнения функции в случае ошибки.

    attempts: количество попыток выполнения функции
    delay: задержка между попытками в секундах
    exceptions: список исключений для обработки (по умолчанию None)
    """
    if exceptions is None:
        exceptions = Exception

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            """
            Обёртка для функции.

            self: экземпляр класса
            args: аргументы функции
            kwargs: ключевые аргументы функции
            """
            for i in range(attempts):
                try:
                    return func(self, *args, **kwargs)
                except exceptions as e:
                    print(f"Попытка № {i + 1}")
                    print(f"Исключение: {e}. Повторная попытка...")
                    time.sleep(delay)
                except Exception as e:
                    raise e

            raise RuntimeError(
                f"В классе {self.__class__.__name__} не удалось выполнить {func.__name__} за {attempts} попыток"
            )

        return wrapper

    return decorator
