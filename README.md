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
Задание check_inheritance_main запускается из корневой дикертории командой
```
python3 ./retry_specific_error/main.py
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

## Задача 3. check_inheritance_main
При помощи api Github невозможно на прямую проверить от какой ветки сделана текущаю и поэтому я придумал алгоритм, который обрабатывает ряд случаев и даёт ответ: создана ветка от майн или от другой ветки. <br/> 
Также чтобы протестить разные ветки можно поменять значение BRANCH в файле [config.py](check_inheritance_main\config.py). <br/> 
Подробности реализации:
Сначала нужно собрать все коммиты из репозитория (по хорошему они должны храниться в базе данных) и собираются подозрительные коммиты, которые уже были опознаны (они существуют для того, что даже после удаления родительской ветки мы могли всё ещё определяться некорректность наследуемых веток) <br/>
Нужно найти подозрительный коммит - коммит является подозрительным, если он присутствует в двух и более ветках. Также нам понадобится хвост комитов после подозрительного. Если подозрительных коммитов нет или в ветки всего 1 коммит то ветка явно сделана от main. <br/>
Далее нужно проверить старые подозрительные коммиты на совпадения, если они есть, то мы можем сразу точно определить от мейна или нет ветка. Также это нас предостерегает от некоторых нежелательных ситуаций в виде, например, удаления ветки. <br/>
Нужно определить хвост у текущий ветки и предыдущий коммит, который нам понадобится, если предыдущего нет, то явно ветка сделана от майн. <br/>
Далее нужно пробежаться по веткам и найти пересечения множеств комитов и сохранить подозрительные ветки. Также требуется отдельно обработать случаи, когда у нас есть цепочка наследования, если этого не сделать, то корректность работы кода будет зависить от того в каком порядке перебираются ветки. Всё что нужно сделать это найти пересечения коммитов и взять первый. <br/>
Нужно сравнить время создания комитов, но делать это нужно для 1 ветки и отдельно для случая когда их множество. Разница заключается в том, что когда веток больше 1, то нужно переопределить подозрительный коммит, что было следано ранее.<br/>
В конце сранивается время создания и возвращается значение.<br/>
### Альтернативное решение
Выше описаный подход требует много вычислительный ресурсов и требуется заранее знать полный набор коммитов, что может быть проблемой. Можно сильно упростить задачу, если анализировать только head каждой ветки, да это посути легко обойти, но мы закрываем один из самых частых случает и к тому же сложность реализации данного подхода низкая
```
        last_commits = set() 

        for branch in branches:
            if branch['name'] != "main":
                last_commits.add(branch['commit']['sha']) 
            if branch['name'] == BRANCH:
                LAST_BRANCH_COM = branch['commit']['sha']

        with open("last_commits.json", "w") as file:
            json.dump(list(last_commits), file, indent=2)

        with open("branches.json", "w") as file:
            json.dump(branches, file, indent=2)
        
        for branch in branches:
            if branch['name'] ==  BRANCH:
                print(f"Branch Name: {branch['name']}")

                commit_response = requests.get(branch['commit']['url'], auth=("RavenDenster", token))
                commit_data = commit_response.json()

                with open("last_commit_info.json", "w") as file:
                    json.dump(commit_data, file, indent=2)

                current_commit_sha = commit_data['sha']
                is_from_other_branch = False
                
                while 'parents' in commit_data and commit_data['parents']:
                   # print(current_commit_sha)
                    if current_commit_sha in last_commits:
                        if current_commit_sha != LAST_BRANCH_COM:
                            is_from_other_branch = True
                            break
                    
                    current_commit_sha = commit_data['parents'][0]['sha']
                    commit_response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits/{current_commit_sha}", auth=("RavenDenster", token))
                    commit_data = commit_response.json()
                
                if is_from_other_branch:
                    print(f"  Эта ветка не была создана от main.")
                else:
                    print(f"  Эта ветка была создана от main.")
```

## Примечания 
Для проверки работоспосбности кода и его тестирования были добавлены мок классы, в которые был добавлен только необходимый функционал для работоспособности
кода. Также в код не относящийся на прямую к решению задач были внесены небольшие изменения, такие как замена common_log на обычный print чтобы видеть 
информацию в терминале.
Также во втором задание был создан доролнительный класс Label который содержит только имя метки это было сделано только для демонстрационных целий, на основной функционал это не влияет.

