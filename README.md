# Dataiku Speech-to-Text Plugin

## Overview

The Dataiku Speech-to-Text Plugin is designed to convert audio files into structured datasets containing transcribed text. This plugin provides a seamless way to integrate speech-to-text functionality into your Dataiku projects, enabling you to analyze and process spoken content efficiently. The plugin is based on the powerful [openai-whisper](https://github.com/openai/whisper) library, ensuring high-quality transcriptions.

## Features

- **Audio File Conversion**: Convert audio files into a dataset containing the path of the audio file and a row per sentence extracted from that file.
- **Flexible Input**: Accepts either a folder containing audio files or a dataset with URLs of audio files.
- **Detailed Output**: Generates a dataset with the path of the audio file, transcribed sentences, and their corresponding start and end times in seconds.
- **Easy Configuration**: Requires minimal setup with only one parameter for specifying the column containing audio file URLs when using a dataset as input.
- **Powered by `openai-whisper`**: Utilizes the `openai-whisper` library for accurate and efficient speech-to-text transcription.

## Installation

To install the Dataiku Speech-to-Text Plugin, follow these steps:

1. Download the plugin package from the [Dataiku Plugin Store](https://github.com/alexbourret/dss-plugin-speech-to-text/releases).
2. In your Dataiku instance, navigate Plugins > Add plugin > Upload and select the downloaded plugin package.
3. Follow the on-screen instructions to complete the installation.

## Usage

### Recipe Configuration

1. **Add Recipe**: In your Dataiku project, add a new recipe and select the Speech-to-Text plugin.
2. **Input Configuration**:
   - If using a folder of audio files, select the folder as the input.
   - If using a dataset with URLs, select the dataset and specify the column containing the audio file URLs.
3. **Output Configuration**: Specify the output dataset where the transcribed text will be stored.

### Output Dataset

The output dataset will contain the following columns:

- `audio_file_path`: The path or URL of the audio file.
- `sentence`: The transcribed sentence extracted from the audio file.
- `start_time`: The start time of the sentence in seconds.
- `end_time`: The end time of the sentence in seconds.

## Example

### Input: Folder of Audio Files

- Folder containing audio files (e.g., `audio_files/`).

### Input: Dataset with URLs

| audio_url                       |
|---------------------------------|
| http://example.com/audio1.mp3   |
| http://example.com/audio2.mp3   |

### Output Dataset

| audio_file_path                | sentence                     | start_time | end_time |
|--------------------------------|------------------------------|------------|----------|
| audio_files/audio1.mp3         | This is the first sentence.  | 0.5        | 2.3      |
| audio_files/audio1.mp3         | Here is another sentence.    | 2.5        | 4.8      |
| http://example.com/audio2.mp3  | Hello, this is a test.       | 1.2        | 3.1      |

## Parameters

- **Column Name for Audio URLs**: (Required if input is a dataset) The name of the column in the input dataset that contains the URLs of the audio files.

## Limitations

- The plugin currently supports audio files in common formats such as MP3, WAV, etc.
- Ensure that the audio files are accessible and properly formatted for accurate transcription.

## Support

For any issues or feature requests, please contact the plugin maintainer or open an issue on the [plugin's GitHub repository](https://github.com/alexbourret/dss-plugin-speech-to-text/issues).

---

This README provides a comprehensive guide to using the Dataiku Speech-to-Text Plugin. If you have any questions or need further assistance, feel free to reach out!
