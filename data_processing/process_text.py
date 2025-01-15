import os
import re

def remove_commas_in_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Traverse the input folder and its subdirectories
    for root, dirs, files in os.walk(input_folder):
        # Determine the relative path of the current folder
        relative_path = os.path.relpath(root, input_folder)
        # Create corresponding subdirectories in the output folder
        current_output_folder = os.path.join(output_folder, relative_path)
        os.makedirs(current_output_folder, exist_ok=True)
        
        # Process each file in the current directory
        for filename in files:
            if filename.endswith('.txt'):  # Process only .txt files
                input_file_path = os.path.join(root, filename)
                output_file_path = os.path.join(current_output_folder, filename)
                
                # Read and process the file
                with open(input_file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # # Remove commas
                # modified_content = content.replace(',', '')

                # Remove commas and spaces before commas
                modified_content = re.sub(r'\s*,', '', content)
                
                # Save the modified content to the output file
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(modified_content)
    
    print(f"All files processed. Modified files are saved in '{output_folder}'.")

# Function to split a text file into separate files for each line
def split_txt_file(input_file, output_dir, id):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open the input file and read lines
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Save each line into a separate file
    for index, line in enumerate(lines):
        output_filename = f"{id}_{index:04d}.txt"  # Format as 0000.txt, 0001.txt, etc.
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'w') as output_file:
            output_file.write(line)

if __name__ == '__main__':
    # Example usage:
    input_folder = '/mnt/lore/research/projects/long_form_tts/data/rs_parallel_e2e_testing/comma_rich_samples_en_gb/text'
    output_folder = '/mnt/lore/research/projects/long_form_tts/data/rs_parallel_e2e_testing/comma_rich_samples_en_gb/text_without_comma'
    remove_commas_in_folder(input_folder, output_folder)
