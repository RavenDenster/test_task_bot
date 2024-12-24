from retry_decorator import retry_decorator 
import random

class MockClass:
    def __init__(self, name):
        self.name = name

    @retry_decorator(attempts=10, delay=1, exceptions=(ValueError, OverflowError))
    def unreliable_method(self):
        rand_val = random.random()
        if rand_val < 0.3:
            raise ValueError("ValueError")
        elif 0.3 <= rand_val < 0.9:
            raise OverflowError("OverflowError")
        elif rand_val >= 0.9:
            raise SyntaxError("SyntaxError")

if __name__ == "__main__":
    my_instance = MockClass("ex")

    try:
        result = my_instance.unreliable_method()
        print(result)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
