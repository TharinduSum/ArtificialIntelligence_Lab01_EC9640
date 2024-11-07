import Levenshtein
import pandas as pd

# Function to load the misspellings from a file
def load_misspellings(file_path):
    misspellings = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(":")
            correct_word = parts[0].strip()
            misspelled_words = parts[1].strip().split()
            misspellings[correct_word] = misspelled_words
    return misspellings

# Function to calculate Levenshtein similarity (accuracy) between words
def calculate_accuracy(original_word, corrected_word):
    distance = Levenshtein.distance(original_word, corrected_word)
    max_len = max(len(original_word), len(corrected_word))
    return 1 - (distance / max_len)

# Function to find closest matching word using Levenshtein distance
def find_closest_word(input_word, misspellings):
    closest_word = None
    min_distance = float('inf')
    
    for correct_word, misspelled_words in misspellings.items():
        # Check the distance between the input and the correct word
        dist_to_correct = Levenshtein.distance(input_word, correct_word)
        if dist_to_correct < min_distance:
            closest_word = correct_word
            min_distance = dist_to_correct
        
        # Check the distance between the input and misspelled words
        for misspelled in misspelled_words:
            dist_to_misspelled = Levenshtein.distance(input_word, misspelled)
            if dist_to_misspelled < min_distance:
                closest_word = correct_word
                min_distance = dist_to_misspelled
    
    return closest_word

# Main function to handle user input and find correct word
def main():
    file_path = 'wikipedia_misspells.txt'  # Path to the file
    misspellings = load_misspellings(file_path)

    # Get user input
    user_input = input("Enter words separated by commas: ").strip()
    words = user_input.split(',')

    results = []

    # Initialize counters for Precision and Recall
    true_positives = 0
    total_inputs = len(words)
    total_correct_words = sum(len(v) + 1 for v in misspellings.values())  # Total correct words in the misspellings list

    # For each word in the input, find the closest matching correct word
    for word in words:
        word = word.strip()  # Clean up any extra spaces
        closest_word = find_closest_word(word, misspellings)
        
        # Calculate accuracy (Levenshtein similarity)
        accuracy = calculate_accuracy(word, closest_word)
        
        # Check if the word is correctly matched
        is_correct = closest_word in misspellings and word != closest_word
        
        if is_correct:
            true_positives += 1
        
        results.append({
            "Original": word,
            "Corrected": closest_word,
            "Accuracy": accuracy,
            "Precision": true_positives / total_inputs if total_inputs > 0 else 0,
            "Recall": true_positives / total_correct_words if total_correct_words > 0 else 0
        })
    
    # Convert results to DataFrame for better table display
    df = pd.DataFrame(results)
    print(df)

if __name__ == '__main__':
    main()
