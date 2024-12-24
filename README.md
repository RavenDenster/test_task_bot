# Отчёт по проделанной работе

## Запуск
Задание retry_specific_error запускается из корневой дикертории командой
```
python3 ./retry_specific_error/main.py
```
Задание label_bug запускается из корневой директории командой
```
python3 ./label_bug/main.py
```

## Задача 1. retry_specific_error
Для реализации задачи был добавлин в декоратор с параметрами дополнительный параметр exceptions, который находится в файле [retry_decorator.py](retry_specific_error/retry_decorator.py). По умолчанию он равен None и в таком случае к данному параметру присваивается общий объект ошибки Exception. Если передан картеж из возможных ошибок, то в цикле будут обрабатываться только они. В случае возникновения непредвиденной ошибка она сразу выкидывается наверх.<br/> 
Также в файле [main.py](retry_specific_error/main.py) находится пример работы этого декоратора на примере функции, которая рандомно генерирует ошибки.
### Альтернативное решение
Возможно в некоторых случаях было бы уместно даже при условии появления непредвиденной ошибки завершать все попытки в цикле. Для этого можно сделать список unhandled_exceptions и только в конце выбросить наверх исключение:
```
unhandled_exceptions = []

            for i in range(attempts):
                try:
                    return func(self, *args, **kwargs)
                except exceptions as e:
                    print(f"Попытка № {i + 1}")
                    print(f"Исключение: {e}. Повторная попытка...")
                    time.sleep(delay)
                except Exception as e:
                    unhandled_exceptions.append(e)

            if unhandled_exceptions:
                raise unhandled_exceptions[0]
```
Данная реализация возможна если этот декоратор будет работать с функциями, которые обрабатывают, например, сетивые запрос, но данная реализация не соответсвует дз

## Задача 2. label_bug
Для реализации данной задачи был изменён метод add_labels_to_pull_request и добавлен remove_non_compliant_labels в файле [label_manager.py](label_bug/label_manager.py). В методе add_labels_to_pull_request добавлен вызов функции remove_non_compliant_labels в которую передаётся набор устанавливаемых меток и сам пулл-реквест. Метод remove_non_compliant_labels удаляет метки из пулл-реквеста, которые не соответствуют новому списку меток и имеют флаг removable. Также к классу PullRequest был добавлен метод remove_labels, который выполняет удаление меток из конкретного пулл-реквеста. Сделано был это из логических соображений, так как у класса есть метод add_labels, но нет метода remove_labels. <br/> 
В файле [mock_class.py](label_bug/mock_class.py) хранятся классы, которые были написаны для проверки работоспособности и тестирования кода.<br/> 
В файле [main.py](label_bug/main.py) показательный пример работы программы, тепере метки удаляются не полностью, а только те которые не нужно ставить при вызове функции добавления
### Альтернативное решение
Можно не создавать новый метод для класса PullRequest, а оставить старую реализацию
```
        original_number = len(pull_request_labels)
        for label_data in AVAILABLE_LABELS.values():
            if label_data.name in pull_request_labels and label_data.removable:
                if label_data.name not in keys:
                    pull_request_labels.remove(label_data.name)

        if original_number != len(pull_request_labels):
            pull_request.set_labels(pull_request_labels)
```
Также вызов функции remove_non_compliant_labels можно делать не в функции add_labels_to_pull_request, а в классе отвечающего за проверку пулл-реквеста в методе set_conclusion.

## Примечания 
Для проверки работоспосбности кода и его тестирования были добавлены мок классы, в которые был добавлен только необходимый функционал для работоспособности
кода. Также в код не относящийся на прямую к решению задач были внесены небольшие изменения, такие как замена common_log на обычный print чтобы видеть 
информацию в терминале.
