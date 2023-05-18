import os
import time
from matplotlib import pyplot as plt


def build_bar_chart(data, file_name, title="Grouped Bar Chart", x_axis="Groups", y_axis="Count"):
    keys = list(data.keys())
    values = list(data.values())

    # Create the bar chart using matplotlib
    fig, ax = plt.subplots()

    # Plot the bars
    ax.bar(keys, values)

    # Add labels and title
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    ax.set_xticks(keys)

    # Display the chart
    os.makedirs(file_name + '/', exist_ok=True)   
    plt.savefig(file_name + f'/{time.time()}.png')


def build_grouped_bar_chart(data, file_name, title="Grouped Bar Chart", x_axis="Groups", y_axis="Count"):
    # data = {10: {2: 3, 1: 1}, 20: {2: 4}, 40: {2: 3, 1: 1}, 70: {2: 2, 1: 2}}
    print("data", data)

    # Extract the keys and values from the dictionary
    groups = list(data.keys())
    # choices = list(data[groups[0]].keys())
    choices = sorted(
        list(set(sum((list(i.keys()) for i in data.values()), []))))

    # Prepare the data for plotting
    bar_width = 0.7/len(choices)
    opacity = 0.8
    index = range(len(groups))

    # Create the grouped bar chart
    fig, ax = plt.subplots()
    for i, choice in enumerate(choices):
        counts = [data[group].get(choice, 0) for group in groups]
        rects = ax.bar([x + (i * bar_width) for x in index],
                    counts, bar_width, alpha=opacity, label=choice)

    # Add labels and title
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    print([x + (len(choices) * bar_width) / 2 for x in index])
    ax.set_xticks([x + (len(choices) * bar_width) / 2 for x in index])
    ax.set_xticklabels([str(x) for x in groups])
    ax.legend(title="Choice")

    plt.tight_layout()
    os.makedirs(file_name + '/', exist_ok=True)    
    plt.savefig(file_name + f'/{time.time()}.png')