
import json
import statistics
import matplotlib.pyplot as plt
import numpy as np

from models.Task import Task
from models.Annotator import Annotator

with open("references/anonymized_project.json") as f:
    data = json.load(f)

results = data["results"]["root_node"]["results"]
tasks = []
annotators_dict = {}
annotators = []

for work_package_id in results:
    serialized_tasks = results[work_package_id]['results']
    for serialized_task in serialized_tasks:
        tasks.append(Task.deserialize(serialized_task))

for task in tasks:
    if task.annotator_id not in annotators_dict:
        annotators_dict[task.annotator_id] = []
    annotators_dict[task.annotator_id].append(task)

for annotator_id in annotators_dict:
    annotator_tasks = annotators_dict[annotator_id]
    annotators.append(Annotator(annotator_tasks[0].annotator_id,
                                annotator_tasks))

print("Question 1")

print("1.a")
total_annotators_count = len(annotators)
print("Number of annotators: " + str(total_annotators_count))

print("1.b")

annotation_times = []
annotation_times_without_outliers = []
for annotator in annotators:
    for task in annotator.tasks:
        annotation_times.append(task.duration)
        if task.duration > 0 and task.duration < 5000:
            annotation_times_without_outliers.append(task.duration)

print("Minimum annotation time: " + str(min(annotation_times)) + "ms")
print("Maximum annotation time: " + str(max(annotation_times)) + "ms")
print("Average annotation time: " + str(statistics.mean(annotation_times)) + "ms")
print("Average annotation time without outliers: " +
      str(statistics.mean(annotation_times_without_outliers)) + "ms")
print("Median annotation time: " +
      str(statistics.median(annotation_times)) + "ms")

plt.hist(annotation_times, bins=100)
plt.title("Annotation time per task")
plt.ylabel("Task count")
plt.xlabel("Annotation time (ms)")
plt.tight_layout()
plt.savefig("plots/question_1_b.png")

plt.clf()
plt.hist(annotation_times_without_outliers, bins=100)
plt.title("Annotation time per task (without outliers)")
plt.ylabel("Task count")
plt.xlabel("Annotation time (ms)")
plt.tight_layout()
plt.savefig("plots/question_1_b_no_outliers.png")

print("1.c")
number_of_tasks_per_annotator = []
for annotator in annotators:
    number_of_tasks_per_annotator.append(len(annotator.tasks))

print("Minimum number of tasks per annotator: " +
      str(min(number_of_tasks_per_annotator)))
print("Maximum number of tasks per annotator: " +
      str(max(number_of_tasks_per_annotator)))

bar_chart_x = []
bar_chart_y = []
for annotator in annotators:
    bar_chart_x.append(annotator.id)
    result_count = len(annotator.tasks)
    bar_chart_y.append(result_count)

plt.clf()
plt.title("Number of results per annotator")
plt.ylabel("Result count")
plt.xlabel("Annotator id")
plt.bar(bar_chart_x, bar_chart_y)
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.tight_layout()
plt.savefig("plots/question_1_c.png")

print("1.d")
input_answers_dict = {}
for annotator in annotators:
    for task in annotator.tasks:
        if task.input_id not in input_answers_dict:
            input_answers_dict[task.input_id] = []
        input_answers_dict[task.input_id].append(int(task.answer))

inputs_with_high_variance_results_count = 0
for input_id in input_answers_dict:
    input_variance = np.var(input_answers_dict[input_id])
    high_variance = 0.2
    if input_variance > high_variance:
        inputs_with_high_variance_results_count += 1

print("Out of " + str(len(input_answers_dict)) + " distinct inputs, " +
      str(inputs_with_high_variance_results_count) + " of them have a high variance")

print("Question 2")

print("2.a")
tasks_that_cannot_be_solved = []
tasks_with_corrupt_data = []
total_task_count = 0
annotator_ids = []

for annotator in annotators:
    for task in annotator.tasks:
        total_task_count += 1
        if task.cant_solve:
            tasks_that_cannot_be_solved.append(task)
            annotator_ids.append(annotator.id)
        if task.corrupt_data:
            tasks_with_corrupt_data.append(task)
            annotator_ids.append(annotator.id)

durations = []
for task in tasks_that_cannot_be_solved:
    durations.append(task.duration)
tasks_that_cannot_be_solved_average_duration = statistics.mean(durations)

durations = []
for task in tasks_with_corrupt_data:
    durations.append(task.duration)
tasks_with_corrupt_data_average_duration = statistics.mean(durations)

print("Out of " + str(total_task_count) + " tasks, " +
      str(len(tasks_that_cannot_be_solved)) + " of them could not be solved")
print("Out of " + str(total_task_count) + " tasks, " +
      str(len(tasks_with_corrupt_data)) + " of them had corrupt data")

print("Average duration of tasks that could not be solved: " + str(tasks_that_cannot_be_solved_average_duration) + "ms")
print("Average duration of tasks with corrupt data: " + str(tasks_with_corrupt_data_average_duration) + "ms")

print("Annotators who reported tasks that could not be solved or with corrupt data:")
print(np.unique(annotator_ids))

print("Question 3")

with open("references/references.json") as f:
    references_json = json.load(f)

references_dict = {}
references = []
for img_id in references_json:
    is_bicycle = references_json[img_id]["is_bicycle"]
    references_dict[img_id] = is_bicycle
    references.append(int(is_bicycle))

references = np.array(references)
is_bicycles = (references == 0).sum()
is_not_bicycles = (references == 1).sum()

plt.clf()
plt.title("Repartition of the references values for each input")
plt.pie([is_bicycles, is_not_bicycles], labels=[
        "True", "False"], autopct="%1.1f%%")
plt.tight_layout()
plt.savefig("plots/question_3.png")

print("Question 4")
annotator_performances = {}
annotator_accuracy_rates = []

for annotator in annotators:
    durations = []
    for task in annotator.tasks:
        durations.append(task.duration)
    avg_duration = statistics.mean(durations)
    accuracy_rate = annotator.get_accuracy_rate(references_dict)
    annotator_accuracy_rates.append(accuracy_rate)
    annotator_performances[annotator.id] = {}
    annotator_performances[annotator.id]['accuracy_rate'] = round(
        accuracy_rate * 100, 2)
    annotator_performances[annotator.id]['avg_duration'] = round(avg_duration)

print(annotator_accuracy_rates)
print(statistics.mean(annotator_accuracy_rates))

# Best performing annotators
# for annotator in sorted(annotator_performances, key=lambda annotator: annotator_performances[annotator]['accuracy_rate'], reverse=True):
#     print(annotator + " & " + str(annotator_performances[annotator]['accuracy_rate']) + " & " + str(
#         annotator_performances[annotator]['avg_duration']) + " \\\\")

# Worst performing annotators
# for annotator in sorted(annotator_performances, key=lambda annotator: annotator_performances[annotator]['accuracy_rate']):
#     print(annotator + " & " + str(annotator_performances[annotator]['accuracy_rate']) + " & " + str(annotator_performances[annotator]['avg_duration']) + " \\\\")

plt.clf()
plt.hist(annotator_accuracy_rates)
plt.title("Annotator accuracy rates")
plt.ylabel("Frequency")
plt.xlabel("Accuracy")
plt.tight_layout()
plt.savefig("plots/question_4.png")


x = []
y = []

for annotator_id in annotator_performances:
    average_duration = annotator_performances[annotator_id]['avg_duration']
    # Ignore outlier values
    if average_duration > 0:
        x.append(annotator_performances[annotator_id]['accuracy_rate'])
        y.append(annotator_performances[annotator_id]['avg_duration'])

plt.clf()
plt.scatter(x, y)
plt.title("Annotator accuracy versus average task duration time")
plt.ylabel("Average duration")
plt.xlabel("Accuracy")
plt.tight_layout()
plt.savefig("plots/question_4_e.png")

# Ranking with points

task_average_durations_dict = {}

for annotator in annotators:
    durations = []
    for task in annotator.tasks:
        if task.input_id not in task_average_durations_dict:
            task_average_durations_dict[task.input_id] = []
        task_average_durations_dict[task.input_id].append(task.duration)

for input_id in task_average_durations_dict:
    task_average_durations_dict[input_id] = statistics.mean(task_average_durations_dict[input_id])

def get_task_points(task):
    correct_answer = references_dict[task.input_id]
    is_answer_correct = task.answer == correct_answer

    if not is_answer_correct:
        return 0

    average_task_duration = task_average_durations_dict[task.input_id]
    correct_answers_number = input_answers_dict[task.input_id].count(correct_answer)
    task_duration = task.duration

    if task.duration <= 0:
        task_duration = average_task_duration
    task_completion_percentage = 0

    if correct_answers_number > 0:
        task_completion_percentage = (len(input_answers_dict[task.input_id]) / correct_answers_number) / 100

    return 10 * (average_task_duration / task_duration) * (1 + (1 - pow(task_completion_percentage, 2)))

annotator_points = []

for annotator in annotators:
    points = []
    for task in annotator.tasks:
        points.append(get_task_points(task))
    annotator_points.append([annotator.id, round(statistics.mean(points), 2)])

annotator_points.sort(key=lambda x: x[1], reverse=True)

# Best performing annotators based on accuracy, task duration and task difficulty sorted in descending order
for annotator in annotator_points:
    print(annotator[0] + " & " + str(annotator[1]) + " \\\\")