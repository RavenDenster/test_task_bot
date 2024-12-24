from typing import List, Union

class Repository:
    def __init__(self):
        self.labels = []

    def get_labels(self):
        return self.labels

    def create_label(self, name: str,  color: str, description: str):
        if not any(label.name == name for label in self.labels):
            new_label = LabelData(name, color, description)
            self.labels.append(new_label)

    def remove_label(self, name: str):
        self.labels = [label for label in self.labels if label.name != name]

class LabelData:
    def __init__(
        self, name: str, color: str, description: str, removable: bool = False
    ):
        self.name = name.lower()
        self.color = color
        self.description = description
        self.removable = removable
    
    def update(self, name: str, description: str, color: str):
        self.name = name
        self.description = description
        self.color = color
        
class Label:
    def __init__(self, name: str):
        self.name = name

class PullRequest:
    def __init__(self):
        self._labels = []

    def get_labels(self) -> List[Label]:
        """Возвращает текущие метки пулл-реквеста."""
        return self._labels

    def set_labels(self, labels: List[str]) -> None:
        """Устанавливает новые метки для пулл-реквеста, заменяя существующие."""
        self._labels = [Label(name) for name in labels]

    def add_labels(self, labels: List[str]) -> None:
        """Добавляет метки к пулл-реквесту."""
        for label in labels:
            print(f"Добавляем метку: {label}")
            if label not in [l.name for l in self._labels]:
                self._labels.append(Label(label))
                
    def remove_labels(self, labels_to_remove: Union[str, List[str]]) -> None:
        """Удаляет метки из пулл-реквеста."""
        labels_to_remove = labels_to_remove if isinstance(labels_to_remove, list) else [labels_to_remove]
        current_labels = [label.name for label in self.get_labels()]

        for remove_label in labels_to_remove:
            if remove_label in current_labels:
                print(f"Удаляем метку: {remove_label}")
                for label in self._labels:
                    if remove_label == label.name:
                        self._labels.remove(label)
            else:
                print(f"Метка {remove_label} не найдена в текущем списке меток.")