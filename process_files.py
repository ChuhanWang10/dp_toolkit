import os
import librosa
from process_audio import detect_short_audios, get_duration

def delete_short_wav_files(dirpath, threshold):
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.lower().endswith('.wav'):
                # print(os.path.relpath(os.path.join(root, file), dirpath))
                wavpath = os.path.join(root, file)
                sampling_rate = librosa.get_samplerate(wavpath)
                duration = get_duration(wavpath,sampling_rate)
                if duration < threshold:
                    print(f"Delete {wavpath}: {duration} seconds")
                    os.remove(wavpath)

def find_single_file_subfolder(root_dirpath):
    single_file_subfolder = []
    for dirpath, dirnames, filenames in os.walk(root_dirpath):
        # Skip the root folder itself
        if dirpath != root_dirpath:
            # Find only the lowest-level subfolders
            if not dirnames:
                file_count = len(filenames)
                if file_count <= 1:
                    print(f"Subfolder: {dirpath}") 
                    print(f"Number of files: {file_count}\n") 
                    single_file_subfolder += dirpath



if __name__ == '__main__':
    folder_path = "/home/chuwan/data/LibriTTS_R_16k/train-clean-100"
    #folder_path = "/home/chuwan/experiments/knn-vc/data/rsvc_real/rsvc_real_16k"
    #detect_short_audios(folder_path, threshold=1)

    find_single_file_subfolder(folder_path)