class Task:

    def __init__(self, input_id, created_at, answer, cant_solve, corrupt_data, duration):
        self.input_id = input_id
        self.created_at = created_at
        self.answer = answer
        self.cant_solve = cant_solve
        self.corrupt_data = corrupt_data
        self.duration = duration

    @staticmethod
    def parse_input_id_from_image_url(url):
        """
        Parses the given url to extract the input id.
        e.g: the url "https://qm-auto-annotator.s3.eu-central-1.amazonaws.com/bicycles/img_4686.jpg" will return the string "img_4686"
        """
        return url.split('/')[-1].split('.')[0]

    @staticmethod
    def deserialize(serializedTask):
        """
        Deserializes the given serialized task under a dict format to a Task instance.
        Example of a serialized task:
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
        """
        return Task(Task.parse_input_id_from_image_url(serializedTask['task_input']['image_url']),
                    serializedTask['created_at'],
                    str(serializedTask['task_output']['answer']).lower() in ("yes", "true", "t", "1"),
                    serializedTask['task_output']['cant_solve'],
                    serializedTask['task_output']['corrupt_data'],
                    serializedTask['task_output']['duration_ms'])
