import os
import matplotlib.pyplot as plt
import numpy as np

# Configuratie: definieer de modellen en hun bestandsnamen
models = [
    {"name": "Rockyou", "filename": "battlefieldrockyou{}_results.txt", "color": "b", "marker": "o", "linestyle": "-"},
    {"name": "Wikiscraper", "filename": "battlefieldscrape{}_results.txt", "color": "r", "marker": "s", "linestyle": "-"},
    {"name": "Llama3.1", "filename": "battlefieldllama31{}_results.txt", "color": "green", "marker": "^", "linestyle": "-"},
    {"name": "PCFG-Wikiscraper", "filename": "battlefieldscrapepcfg{}_results.txt", "color": "r", "marker": "s", "linestyle": "--"},
    {"name": "PCFG-Llama3.1", "filename": "battlefieldllamapcfg{}_results.txt", "color": "green", "marker": "^", "linestyle": "--"}
]

folder_path = './'  # Pas dit aan naar het juiste pad

data = {model["name"]: {"x": [0], "y": [0]} for model in models}
overlap_data = {"Scrape vs Rockyou": {"x": [0], "y": [0]},
               "Llama vs Rockyou": {"x": [0], "y": [0]},
               "Llama vs Scrape": {"x": [0], "y": [0]}}

# Verzamelen van data
for i in range(1, 11):
    sets = {}
    for model in models:
        file_path = os.path.join(folder_path, model["filename"].format(i * 1000))
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                sets[model["name"]] = set(file.read().splitlines())
            data[model["name"]]["x"].append(i * 1000)
            data[model["name"]]["y"].append(len(sets[model["name"]]))
    
    # Bereken overlap
    if "Rockyou" in sets and "Scrape" in sets:
        percentage = 100 * (len(sets["Scrape"] - sets["Scrape"].intersection(sets["Rockyou"])) / 
                            len(sets["Scrape"].union(sets["Rockyou"])))
        overlap_data["Scrape vs Rockyou"]["x"].append(i * 1000)
        overlap_data["Scrape vs Rockyou"]["y"].append(percentage)
    
    if "Rockyou" in sets and "Llama" in sets:
        percentage = 100 * (len(sets["Llama"] - sets["Llama"].intersection(sets["Rockyou"])) / 
                            len(sets["Llama"].union(sets["Rockyou"])))
        overlap_data["Llama vs Rockyou"]["x"].append(i * 1000)
        overlap_data["Llama vs Rockyou"]["y"].append(percentage)
    
    if "Scrape" in sets and "Llama" in sets:
        percentage = 100 * (len(sets["Llama"] - sets["Llama"].intersection(sets["Scrape"])) / 
                            len(sets["Llama"].union(sets["Scrape"])))
        overlap_data["Llama vs Scrape"]["x"].append(i * 1000)
        overlap_data["Llama vs Scrape"]["y"].append(percentage)

# Plotfunctie
rule = 4841
hashtotal = 292115

def plot_recoveries():
    plt.figure(figsize=(10, 6))
    for model in models:
        plt.plot(np.array(data[model["name"]]["x"]) * rule,
                 100 * np.array(data[model["name"]]["y"]) / hashtotal,
                 marker=model["marker"], linestyle=model["linestyle"],
                 color=model["color"], label=f'{model["name"]} list of length $n$')
    
    plt.title('Battlefield Leak Recovery with the OneRuleToRuleThemStill Ruleset', fontsize=14)
    plt.xlabel('Recovery Attempts (4841 × n)', fontsize=12)
    plt.ylabel('Passwords Recovered (%)', fontsize=12)
    plt.grid(True)
    plt.legend(fontsize=9, loc='best')
    plt.show()

def plot_uniqueness():
    plt.figure(figsize=(10, 6))
    for key, values in overlap_data.items():
        plt.plot(np.array(values["x"]) * rule, values["y"], marker='o', linestyle='-', label=key)
    
    plt.title('Percentage of Unique Passwords recovered per Method', fontsize=14)
    plt.xlabel('Recovery Attempts (4841 × n)', fontsize=12)
    plt.ylabel('Unique Recovered Passwords (%)', fontsize=12)
    plt.grid(True)
    plt.legend(fontsize=11, loc='best')
    plt.show()

# Aanroepen van functies
plot_recoveries()
# plot_uniqueness()
