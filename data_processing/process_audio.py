import os
import wave
import numpy as np
from scipy.io.wavfile import read, write
import soundfile as sf
import librosa
from matplotlib import pyplot as plt
import scipy

# obtain the sampling rate of a wav
def get_sampling_rate(filepath):
    with wave.open(filepath, 'rb') as wav_file:
        sampling_rate = wav_file.getframerate()
        return sampling_rate

# load wav via librosa, scipy or soundfile    
def load_wav_librosa(wavpath):
    # return sampling_rate, wav
    wav, sampling_rate = librosa.core.load(wavpath, sr=None)
    return wav, sampling_rate

def load_wav_scipy(wavpath):
    # return sampling_rate, wav
    MAX_WAV_VALUE = 32768.0 #2**15
    sampling_rate, wav = scipy.io.wavfile.read(wavpath)
    wav = wav / MAX_WAV_VALUE
    return sampling_rate, wav

def load_wav_soundfile(wavpath):
    # return wav, sampling_rate
    wav, sampling_rate = sf.read(wavpath)
    return wav, sampling_rate

def get_duration(wavpath):
    sampling_rate = get_sampling_rate(wavpath)
    return librosa.get_duration(path=wavpath, sr=sampling_rate)

def get_total_duration(dirpath):
    total_duration = 0
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.lower().endswith('.wav'):
                wavpath = os.path.join(root, file)
                duration = get_duration(wavpath)
                total_duration += duration
    print(f"total duration: {total_duration:.2f} seconds, {total_duration/60:.2f} minutes")
    
    return total_duration

def get_durations(dirpath):
    from scipy.io import wavfile
    """get a list of durations 
    """

    durations = []
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.lower().endswith('.wav'):
                wavpath = os.path.join(root, file)
                duration = get_duration(wavpath)
                durations.append(duration)
    
    return durations


def plot_duration_distribution(durations, bin_size=1):
    """plot the distribution of a list of durations

    Args:
        durations (list): a list of durations for each audio file in the dataset
        bin_size (int, optional): bins for distribution in seconds. Default to 1 second
    """
    bins = np.arange(0, max(durations) + bin_size, bin_size)
    total_files = len(durations)

    plt.hist(durations, bins=bins, edgecolor='black', alpha=0.7)
    plt.title(f"Duration Distribution of WAV Files (Total: {total_files})")
    plt.xlabel("Duration (seconds)")
    plt.ylabel("Number of Files")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adding a text annotation
    plt.text(
        0.95, 0.95,
        f"Total Files: {total_files}",
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment='top',
        horizontalalignment='right',
        bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5')
    )
    
    plt.show()

def detect_short_audios(dirpath, threshold):
    files_under_threshold = []
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.lower().endswith('.wav'):
                wavpath = os.path.join(root, file)
                sampling_rate = librosa.get_samplerate(wavpath)
                duration = get_duration(wavpath,sampling_rate)
                if duration < threshold:
                    print(f"{wavpath}: {duration} seconds")
                    files_under_threshold.append(wavpath)
    
    print(f"{len(files_under_threshold)} files are shorter than {threshold} second.")

def detect_long_pauses(wavpath, threshold, pause_duration_threshold):
    # Load the audio file
    audio_signal, sample_rate = librosa.load(wavpath, sr=None)

    # Calculate the total length of the audio
    total_length = librosa.get_duration(audio_signal, sample_rate)

    # Calculate energy or amplitude
    window_size = int(sample_rate * 1)  # 1 second window 
    stride = int(sample_rate * 0.1)  # 0.1 second stride 

    energies = [
        np.sum(audio_signal[i:i + window_size] ** 2)
        for i in range(0, len(audio_signal) - window_size, stride)
    ]

    # Detect pauses larger than a certain duration
    pauses = []
    in_pause = False
    pause_start = 0

    for i, energy in enumerate(energies):
        if energy <= threshold and not in_pause:
            in_pause = True
            pause_start = i * stride / sample_rate
        elif energy > threshold and in_pause:
            pause_end = i * stride / sample_rate
            pause_duration = pause_end - pause_start
            if pause_duration > pause_duration_threshold:
                pauses.append((pause_start, pause_duration))
                in_pause = False
                
    return total_length, pauses

if __name__ == '__main__':
    # get sampling rate
    # filepath = "/home/chuwan/data/LibriSpeech-R/LibriTTS_R/train-clean-100/19/198/19_198_000000_000000.wav"
    # print(f"sampling rate: {get_sampling_rate(filepath)}")

    #get total duration
    folder_path = "/home/chuwan/experiments/knn_vc_all_branches/main/knn-vc/zsvc_testing/rsvc_small/adam_syn"
    print(f"total duration: {get_total_duration(folder_path):.2f} seconds, {get_total_duration(folder_path)/60:.2f} minutes")
    

    # detect wav files shorter than a threshold
    # folder_path = "/home/chuwan/data/LibriTTS_R_16k/train-clean-100"
    # detect_short_audios(folder_path, threshold=0.2)