import os

import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def visualization(filename, filetype):
    # Read the similarity scores from the .npy file
    filepath = filename+filetype
    similarity_scores = np.load(os.getenv("NPYFOLDER_NAME")+filepath)
    filepath = filename + os.getenv("IMG_FILE_TYPE")
    resultpath = os.getenv("RESULT_FILE_PATH")
    # Check if the similarity_scores array is not empty
    if len(similarity_scores) > 0:
        # Calculate statistical measures
        mean_similarity = np.mean(similarity_scores)
        max_similarity = np.max(similarity_scores)
        min_similarity = np.min(similarity_scores)

        # Create a bar chart
        plt.figure(figsize=(8, 6))
        plt.bar(range(len(similarity_scores)), similarity_scores)
        plt.axhline(mean_similarity, color='red', linestyle='--', label='Mean')
        plt.axhline(max_similarity, color='green', linestyle='--', label='Max')
        plt.axhline(min_similarity, color='blue', linestyle='--', label='Min')
        plt.xlabel('Pair Index')
        plt.ylabel('Similarity Score')
        plt.title('Similarity Scores ' + filename)
        plt.legend()
        plt.tight_layout()
        if os.path.exists(resultpath+filepath):
            os.remove(resultpath+filepath)
        # Save the chart as an image file
        plt.savefig(resultpath+filename)

        # Show the chart
        plt.show()
    else:
        print("No similarity scores found. The similarity_scores array is empty.")

    