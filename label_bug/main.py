from label_manager import LabelManager
from mock_class import Repository, PullRequest
    
if __name__ == "__main__":

    mock_repo = Repository()

    label_manager = LabelManager(mock_repo)

    label_manager.create_all_labels_in_repository()

    for label in mock_repo.get_labels():
        print(f"Label: {label.name}, Description: {label.color}, Color: {label.description}")

    pull_request = PullRequest()
    label_manager.add_labels_to_pull_request(pull_request, ["moodle+", "failed", "passed", "duplicate"])

    label_manager.add_labels_to_pull_request(pull_request, ["deadline-", "moodle+", "failed", "proctoring-"])

    label_manager.add_labels_to_pull_request(pull_request, ["moodle+", "failed", "proctoring-"])

    for i in range(len(pull_request.get_labels())):
        print(pull_request.get_labels()[i].name)