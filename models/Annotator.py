import statistics
from models.Task import Task

class Annotator:

    def __init__(self, id, tasks):
        self.id = id
        self.tasks = tasks

    @staticmethod
    def deserialize(id, serializedAnnotator):
        """
        Deserializes the given serialized annotator under a dict format to an Annotator instance.
        Example of a serialized annotator:
        {
            "results": [
                {
                    "task_input": {
                        "image_url": "https://qm-auto-annotator.s3.eu-central-1.amazonaws.com/bicycles/img_4686.jpg"
                    },
                    "created_at": "2021-02-25T14:08:11.319438+00:00",
                    "workpackage_total_size": 5,
                    "loss": 0.0,
                    "project_node_input_id": "7e8984b6-dff7-4015-865a-b721a2faf681",
                    "project_node_output_id": "0000439a-96ac-4bd4-8753-a4baa229ecf2",
                    "task_output": {
                        "answer": "no",
                        "cant_solve": false,
                        "corrupt_data": false,
                        "duration_ms": 997
                    },
                    "user": {
                        "vendor_id": "vendor_01",
                        "id": "08af8775-a72c-4c59-b60f-9ce7df04fa92",
                        "vendor_user_id": "annotator_12"
                    },
                    "root_input": {
                        "image_url": "https://qm-auto-annotator.s3.eu-central-1.amazonaws.com/bicycles/img_4686.jpg"
                    },
                    "project_root_node_input_id": "7e8984b6-dff7-4015-865a-b721a2faf681"
                }
            ]
        }
        ...
        """
        tasks = []
        for serializedTask in serializedAnnotator['results']:
            tasks.append(Task.deserialize(serializedTask))
        return Annotator(id, tasks)
    
    def get_accuracy_rate(self, references_dict):
        """
        Compares the answers of each task to the given references dictionnary.
        Returns an accuracy rate between 0 and 1.
        """
        task_accuracies = []
        for task in self.tasks:
            task_accuracies.append(int(task.answer == references_dict[task.input_id]))
        return statistics.mean(task_accuracies)