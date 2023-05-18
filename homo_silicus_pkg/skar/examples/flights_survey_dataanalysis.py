import sqlite3
import matplotlib.pyplot as plt

from skar.analysis.numbers import strip_complex

def analyze_results(file_name, additional_tables=[]):
    # Connect to the SQLite database
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()

    # Retrieve the data from the database, table by table
    for i in additional_tables:
        if i == "endowment":
            cursor.execute('SELECT endowment, choice FROM endowment')
            rows = cursor.fetchall()

            # Extract relevant information and organize for plotting
            data = {}
            for row in rows:
                # Assuming the endowment column stores dictionaries as string representations
                endowment = eval(row[0])
                choice = row[1]
                for key, value in endowment.items():
                    if key not in data:
                        data[key] = {}
                    try:
                        choice = int(strip_complex(choice))
                    except:
                        pass
                    if value not in data[key]:
                        data[key][value] = {}
                    if choice not in data[key][value]:
                        data[key][value][choice] = 0
                    data[key][value][choice] += 1
            
            # Create grouped bar graphs using matplotlib
            for e, d in data.items():
                build_grouped_bar_chart(d, title = f"Grouped Bar Chart for {i} - {e}", x_axis = "Groups", y_axis = "Count")
        
        elif i == "temperature":
            cursor.execute(f'SELECT {i}, choice FROM {i}')
            rows = cursor.fetchall()

            # Extract relevant information and organize for plotting
            data = {}
            for row in rows:
                # Assuming the endowment column stores dictionaries as string representations
                value = row[0]
                choice = row[1]
                try:
                    choice = int(strip_complex(choice))
                except:
                    pass
                if value not in data:
                    data[value] = {}
                if choice not in data[value]:
                    data[value][choice] = 0
                data[value][choice] += 1
                
            build_grouped_bar_chart(data, title = f"Grouped Bar Chart for {i}", x_axis = "Groups", y_axis = "Count")
            for e, d in data.items():
                build_bar_chart(d, title = f"Grouped Bar Chart for {i} - {e}", x_axis = "Groups", y_axis = "Count")
        else:
            print(f"Sorry, implementation for {i} is in progress!")

    # Step 5: Close the database connection
    conn.close()



def build_bar_chart(data, title = "Grouped Bar Chart", x_axis = "Groups", y_axis = "Count"):
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
    plt.show()
    
def build_grouped_bar_chart(data, title = "Grouped Bar Chart", x_axis = "Groups", y_axis = "Count"):
    # data = {10: {2: 3, 1: 1}, 20: {2: 4}, 40: {2: 3, 1: 1}, 70: {2: 2, 1: 2}}
    print("data", data)

    # Extract the keys and values from the dictionary
    groups = list(data.keys())
    # choices = list(data[groups[0]].keys())
    choices = sorted(list(set(sum((list(i.keys()) for i in data.values()), []))))
    print(groups)
    print(choices)

    # Prepare the data for plotting
    bar_width = 0.7/len(choices)
    opacity = 0.8
    index = range(len(groups))

    # Create the grouped bar chart
    fig, ax = plt.subplots()
    for i, choice in enumerate(choices):
        counts = [data[group].get(choice, 0) for group in groups]
        rects = ax.bar([x + (i * bar_width) for x in index], counts, bar_width, alpha=opacity, label=choice)

    # Add labels and title
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    print([x + (len(choices) * bar_width) / 2 for x in index])
    ax.set_xticks([x + (len(choices) * bar_width) / 2 for x in index])
    ax.set_xticklabels([str(x) for x in groups])
    ax.legend()

    plt.tight_layout()
    plt.show()
    

def run():
    analyze_results('../homo_silicus_pkg/skar/data/experiment_1684380017.235484.db', additional_tables=["endowment", "temperature"])