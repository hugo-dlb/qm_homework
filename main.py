
import json
import statistics
import matplotlib.pyplot as plt
import numpy as np

from models.Annotator import Annotator

with open("references/anonymized_project.json") as f:
    data = json.load(f)

serialized_annotators = data["results"]["root_node"]["results"]
annotators = []

for annotator_id in serialized_annotators:
    annotators.append(Annotator.deserialize(
        annotator_id, serialized_annotators[annotator_id]))

annotation_times = []
for annotator in annotators:
    for task in annotator.tasks:
        # if task.duration > 0 and task.duration < 10000:
        annotation_times.append(task.duration)

print("Question 1")

print("1.a")
total_annotators_count = len(annotators)
print("Number of annotators: " + str(total_annotators_count))

print("1.b")


def reject_outliers(data, m=2):
    # From https://stackoverflow.com/a/11686764

    return data[abs(data - np.mean(data)) < m * np.std(data)]


print("Minimum annotation time: " + str(min(annotation_times)) + "ms")
print("Maximum annotation time: " + str(max(annotation_times)) + "ms")
print("Average annotation time: " + str(statistics.mean(annotation_times)) + "ms")

plt.hist(annotation_times, bins=100)
plt.title("Annotation time per task")
plt.ylabel("Task count")
plt.xlabel("Annotation time (ms)")
plt.savefig("plots/question_1_b.png")

annotation_times_without_outliers = reject_outliers(np.array(annotation_times))

plt.clf()
plt.hist(annotation_times_without_outliers, bins=100)
plt.title("Annotation time per task (without outliers)")
plt.ylabel("Task count")
plt.xlabel("Annotation time (ms)")
plt.savefig("plots/question_1_b_no_outliers.png")

print("1.c")
number_of_tasks_per_annotator = []
for annotator in annotators:
    number_of_tasks_per_annotator.append(len(annotator.tasks))

print("Minimum number of tasks per annotator: " +
      str(min(number_of_tasks_per_annotator)))
print("Maximum number of tasks per annotator: " +
      str(max(number_of_tasks_per_annotator)))

print("1.d")
input_answers_dict = {}
for annotator in annotators:
    for task in annotator.tasks:
        if task.input_id in input_answers_dict:
            input_answers_dict[task.input_id].append(int(task.answer))
        else:
            input_answers_dict[task.input_id] = [int(task.answer)]

inputs_with_high_variance_results_count = 0
for input_id in input_answers_dict:
    input_variance = np.var(input_answers_dict[input_id])
    high_variance = 0.2
    if input_variance > high_variance:
        inputs_with_high_variance_results_count += 1
        print("Input for which annotators highly disagree: " +
              str(min(input_id)) + " (variance: " + str(input_variance) + ")")

print("Out of " + str(len(input_answers_dict)) + " distinct inputs, " +
      str(inputs_with_high_variance_results_count) + " of them have a high variance")

print("Question 2")

print("2.a")
task_that_cannot_be_solved_count = 0
task_with_corrupt_data_count = 0
total_task_count = 0

for annotator in annotators:
    for task in annotator.tasks:
        total_task_count += 1
        if task.cant_solve:
            task_that_cannot_be_solved_count += 1
        if task.corrupt_data:
            task_with_corrupt_data_count += 1

print("Out of " + str(total_task_count) + " tasks, " +
      str(task_that_cannot_be_solved_count) + " of them could not be solved")
print("Out of " + str(total_task_count) + " tasks, " +
      str(task_with_corrupt_data_count) + " of them had corrupt data")

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
plt.savefig("plots/question_3.png")

print("Question 4")
annotator_accuracy_rates = []
best_performing_annotator_ids = []
worst_performing_annotator_ids = []

for annotator in annotators:
    accuracy_rate = annotator.get_accuracy_rate(references_dict)
    annotator_accuracy_rates.append(accuracy_rate)
    if accuracy_rate > 0.9:
        best_performing_annotator_ids.append(annotator.id)
    elif accuracy_rate < 0.7:
        worst_performing_annotator_ids.append(annotator.id)

print(best_performing_annotator_ids)
print(worst_performing_annotator_ids)
print(statistics.mean(annotator_accuracy_rates))

plt.clf()
plt.hist(annotator_accuracy_rates)
plt.title("Annotator accuracy rates")
plt.ylabel("Frequency")
plt.xlabel("Accuracy")
plt.savefig("plots/question_4.png")