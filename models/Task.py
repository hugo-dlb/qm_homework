class Task:

    def __init__(self, annotator_id, input_id, created_at, answer, cant_solve, corrupt_data, duration):
        self.annotator_id = annotator_id
        self.input_id = input_id
        self.created_at = created_at
        self.answer = answer
        self.cant_solve = cant_solve
        self.corrupt_data = corrupt_data
        self.duration = duration

    def __str__(self):
        return '[' + self.annotator_id + ', ' + self.input_id + ', ' + self.created_at + ', ' + str(self.answer) + ', ' + str(self.cant_solve) + ', ' + str(self.corrupt_data) + ', ' + str(self.duration) + ']'

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
        """
        return Task(serializedTask['user']['id'],
                    Task.parse_input_id_from_image_url(serializedTask['task_input']['image_url']),
                    serializedTask['created_at'],
                    str(serializedTask['task_output']['answer']).lower() in ("yes", "true", "t", "1"),
                    serializedTask['task_output']['cant_solve'],
                    serializedTask['task_output']['corrupt_data'],
                    serializedTask['task_output']['duration_ms'])
