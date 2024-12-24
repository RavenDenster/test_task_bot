from typing import List, Union
from mock_class import Repository, PullRequest, LabelData, Label

AVAILABLE_LABELS = {
    "3": LabelData("3", "2bd600", "3 балла"),
    "2": LabelData("2", "b4fb11", "2 балла"),
    "1": LabelData("1", "f0c205", "1 балл"),
    "0": LabelData("0", "106ea6", "0 баллов"),
    "passed": LabelData("passed", "008000", "Проверка пройдена", True),
    "failed": LabelData("failed", "990000", "Проверка провалена", True),
    "deadline-": LabelData("deadline-", "383838", "PR открыт после дедлайна"),
    "duplicate": LabelData(
        "duplicate", "cfd3d7", "PR для данной работы уже был создан ранее", True
    ),
    "duplicate_allowed": LabelData("duplicate allowed", "9369ff", "Разрешено дублирование PR"),
    "unauthorized_merge": LabelData(
        "unauthorized merge", "ff0000", "Несанкционированный мердж PR"
    ),
    "report_ok": LabelData("report ok", "A3F162", "Проверка отчета пройдена", True),
    "report_failed": LabelData("report failed", "EE2D1A", "Проверка отчета провалена", True),
    "-1": LabelData("-1", "6f17c7", "-1 балл"),
    "moodle+": LabelData("moodle+", "dec24c", "Работа выполнена на moodle", True),
    "teacher_approval": LabelData("teacher approval", "b39cde", "Проверено преподавателем"),
    "report_after_deadline": LabelData(
        "report after deadline", "fbed20",
        "Файлы, не относящиеся к коду, были изменены после дедлайна"
    ),
    "reverted": LabelData("reverted", "8e5ee1", "Выполнен откат pull-request'а"),
    "plagiarism": LabelData("plagiarism", "7c0ca0", "Работа списана"),
    "proctoring-": LabelData("proctoring-", "990000", "Возникли проблемы с прокторингом", True),
    "new_changes": LabelData(
        "new_changes", "e3b014",
        "Есть новые изменения. Требуется проверка преподавателя", True
    ),
    "no_deadline_check": LabelData("no_deadline_check", "252850", "Не проводится проверка дедлайна"),
}

GRADE_LABELS = ["1", "2", "3"]

class LabelManager:
    """
    Данный класс предназначен для работы с метками GitHub

    Аргументы:

    `repository: Repository` - репозиторий, в котором будет проводиться работа с метками
    """
     
    def __init__(self, repository: Repository):
        self._repository = repository

    def get_label_info(self, label_key: str) -> Union[LabelData, None]:
        """
        Получение информации о метке

        Аргументы:

        `label_key: str` - ключ метки из AVAILABLE_LABELS

        Выходные данные:

        `Union[LabelData, None]` - информация о метке, если она была найдена, иначе None
        """
        print(f"Получение информации о метке {label_key}")
        return AVAILABLE_LABELS.get(label_key)

    def create_non_existing_labels_in_repository(self, label_keys: Union[str, List[str]]) -> None:
        """
        Создание меток, недоступных в репозитории

        Аргументы:

        `label_keys: Union[str, List[str]]` - ключ метки (ключи меток) из AVAILABLE_LABELS
        """
        print("Создание недоступных из списка меток")
        repository_labels = {
            label.name: label for label in self._repository.get_labels()
        }
        keys = label_keys if isinstance(label_keys, list) else [label_keys]
        for key in keys:
            label = AVAILABLE_LABELS[key]
            if label.name not in repository_labels.keys():
                self._repository.create_label(
                    label.name, label.description, label.color
                )
            elif (
                (repository_labels[label.name].description != label.description) or
                (repository_labels[label.name].color != label.color)
            ):
                repository_labels[label.name].update(label.name, label.description, label.color)

    def create_all_labels_in_repository(self) -> None:
        """
        Создание всех меток в репозитории из AVAILABLE_LABELS
        """
        self.create_non_existing_labels_in_repository(list(AVAILABLE_LABELS.keys()))

    def remove_non_compliant_labels(self, pull_request: PullRequest, new_label_keys: Union[str, List[str]]) -> None:
        """
        Удаляет метки из пулл-реквеста, которые не соответствуют новому списку меток 
        и имеют флаг removable, установленный в True.

        Аргументы:

        pull_request: PullRequest - пулл-реквест

        label_keys: Union[str, List[str]] - ключ метки (ключи меток) из AVAILABLE_LABELS
        """
        print("Удаление меток из пулл-реквеста")
        pull_request_labels = [label.name for label in pull_request.get_labels()]
        if not pull_request_labels:
            return None

        keys = new_label_keys if isinstance(new_label_keys, list) else [new_label_keys]
        labels_to_remove = []

        for label_data in AVAILABLE_LABELS.values():
            if label_data.name in pull_request_labels and label_data.removable:
                if label_data.name not in keys:
                    labels_to_remove.append(label_data.name)

        if labels_to_remove:
            pull_request.remove_labels(labels_to_remove)

    def add_labels_to_pull_request(     
        self, pull_request: PullRequest, label_keys: Union[str, List[str]]
    ) -> None:
        """
        Добавление меток в пулл-реквест (добавляются только нужные метки)

        Аргументы:

        pull_request: PullRequest - пулл-реквест

        label_keys: Union[str, List[str]] - ключ метки (ключи меток) из AVAILABLE_LABELS
        """
        self.create_non_existing_labels_in_repository(label_keys)
        self.remove_non_compliant_labels(pull_request, label_keys)

        print("Выполняется добавление меток в пулл-реквест")
        pull_request_labels = [label.name for label in pull_request.get_labels()]
        keys = label_keys if isinstance(label_keys, list) else [label_keys]
        labels_to_add = []

        for key in keys:
            label = AVAILABLE_LABELS[key]
            if label.name not in pull_request_labels:
                labels_to_add.append(label.name)

        if labels_to_add:
            pull_request.add_labels(labels_to_add)
    
    def pull_request_has_labels(
        self, pull_request: PullRequest, label_keys: Union[str, List[str]]
    ) -> bool:
        """
        Проверка пулл-реквеста на наличие меток

        Аргументы:

        pull_request: PullRequest - пулл-реквест

        label_keys: Union[str, List[str]] - ключ метки (ключи меток) из AVAILABLE_LABELS

        Выходные данные:

        bool - True - все указанные метки присутствуют, иначе False
        """
        print("Выполняется проверка пулл-реквеста на наличие меток")
        pull_request_labels = [label.name for label in pull_request.get_labels()]
        labels_to_check = label_keys if isinstance(label_keys, list) else [label_keys]
        return all(
            AVAILABLE_LABELS[label_key].name in pull_request_labels
            for label_key in labels_to_check
        )
    
    def pull_request_has_grade(self, pull_request: PullRequest) -> bool:
        """
        Проверка пулл-реквеста на наличие оценки (GRADE_LABELS)

        Аргументы:

        pull_request: PullRequest - пулл-реквест

        Выходные данные:

        bool - True - присутствует метка оценки, иначе False
        """
        print("Выполняется проверка пулл-реквеста на наличие оценки")
        pull_request_labels = [label.name for label in pull_request.get_labels()]
        return any(AVAILABLE_LABELS[key].name in pull_request_labels for key in GRADE_LABELS)
    
    def add_grade_to_pull_request(self, pull_request: PullRequest, grade_key: str) -> None:
        """
        Добавление оценки в пулл-реквест при отсутствии других оценок

        Аргументы:

        pull_request: PullRequest - пулл-реквест

        grade_key: str - ключ оценки

        Выходные данные:

        bool - True - присутствует метка оценки, иначе False
        """
        print("Выполняется попытка добавления оценки в пулл-реквест")
        if not self.pull_request_has_grade(pull_request):
            self.add_labels_to_pull_request(pull_request, grade_key)