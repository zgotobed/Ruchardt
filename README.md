# Data Analysis Pipeline

This pipeline outlines the steps to process video data, extract relevant coordinates, and perform analysis using a sine-fitting method.

## Steps

1. **Capture Video**  
   - Use a phone to record the necessary footage.
   - Ensure good lighting and a stable camera for optimal results.

2. **Upload Video**  
   - Transfer the recorded video to a shared Google Drive folder.
   - Ensure the correct permissions are set for accessibility.

3. **Process Video (`process_video.py`)**  
   - Import the video into `process_video.py`.
   - Adjust cropping parameters and color cutoff as needed.
   - Run the script to extract relevant data points.

4. **Generate CSV File**  
   - The script outputs a CSV file containing the extracted coordinates.
   - Verify the contents to ensure correctness.
   - IMPORTANT NOTE: CLEAR THE CSV FILE AND RERUN IT BEFORE MOVING ONTO THE NEXT STEP

5. **Analyze Data (`fit_sine.ipynb`)**  
   - Import the generated CSV file into `fit_sine.ipynb`.
   - Perform the required sine-fitting analysis.
   - Adjust parameters as needed to improve fit quality.

## Notes
- Ensure all dependencies for `process_video.py` and `fit_sine.ipynb` are installed.
- Keep a log of cropping parameters and color cutoffs for consistency.
- Review output data before proceeding to the next step to ensure data integrity.
