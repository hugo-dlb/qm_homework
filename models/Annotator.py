import statistics

class Annotator:

    def __init__(self, id, tasks):
        self.id = id
        self.tasks = tasks
    
    def get_accuracy_rate(self, references_dict):
        """
        Compares the answers of each task to the given references dictionnary.
        Returns an accuracy rate between 0 and 1.
        """
        task_accuracies = []
        for task in self.tasks:
            task_accuracies.append(int(task.answer == references_dict[task.input_id]))
        return statistics.mean(task_accuracies)