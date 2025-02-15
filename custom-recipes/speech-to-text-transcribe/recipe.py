# -*- coding: utf-8 -*-
import dataiku
import pandas
import whisper
import copy
import requests
import shutil

from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config
from temp_utils import CustomTmpFile
from plugin_details import get_initialization_string
from safe_logger import SafeLogger


logger = SafeLogger("speech-to-text plugin")
logger.info("{}".format(get_initialization_string()))

input_A_names = get_input_names_for_role('input_A_role')
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

output_A_names = get_output_names_for_role('main_output')
output_A_datasets = [dataiku.Dataset(name) for name in output_A_names]

config = get_recipe_config()

# Read recipe inputs
documents_to_process = input_A_datasets[0]
documents_to_process_dataframe = None
folder_handle = None
try:
    documents_to_process_dataframe = documents_to_process.get_dataframe()
except Exception as error_message:
    # Input is not a dataset
    # Could be a folder...
    input_folder = get_input_names_for_role("input_A_role")
    input_A_datasets = [dataiku.Folder(name) for name in input_A_names]
    folder_handle = input_A_datasets[0]

audio_model = whisper.load_model("turbo")

if folder_handle:
    paths = folder_handle.list_paths_in_partition()
    output_rows = []
    for path in paths:
        with folder_handle.get_download_stream(path) as file_to_convert:
            output_row = {}
            output_row['error'] = None
            temporary_cache = CustomTmpFile()
            temporary_location = temporary_cache.get_temporary_cache_dir()
            data_to_convert = file_to_convert.read()
            temporary_file = open(temporary_location.name + path, "wb")
            temporary_file.write(data_to_convert)
            temporary_file.close
            face_encodings = None
            try:
                transcription = audio_model.transcribe(temporary_location.name + path)
            except Exception as error_message:
                output_row['error'] = "{}".format(error_message)
            output_row['audio_file_path'] = path
            segments = transcription.get("segments", [])
            for segment in segments:
                speech_row = copy.deepcopy(output_row)
                speech_row['start_time'] = segment.get("start")
                speech_row['end_time'] = segment.get("end")
                speech_row['sentence'] = segment.get("text")
                output_rows.append(speech_row)

    output_dataframe = pandas.DataFrame(output_rows)
    output_A_datasets[0].write_with_schema(output_dataframe)
else:
    urls_column_name = config.get("url_column")
    if not urls_column_name:
        raise Exception("The column containing the documents URl must be selected")

    output_rows = []
    temporary_cache = CustomTmpFile()
    temporary_location = temporary_cache.get_temporary_cache_dir()
    for index, input_row in documents_to_process_dataframe.iterrows():
        output_row = {}
        output_row = input_row
        output_row['error'] = None
        url = input_row[urls_column_name]
        face_encodings = None
        speech_row = {}
        try:
            response = requests.get(url, stream=True)
            file_name = url.split('/')[-1]
            file_path = "/".join([temporary_location.name, file_name])
            logger.info("Creating temporary file '{}'".format(file_path))
            response.raw.decode_content = True
            with open(file_path, 'wb') as file_handle:
                shutil.copyfileobj(response.raw, file_handle)
            transcription = audio_model.transcribe(file_path)
            segments = transcription.get("segments", [])
            for segment in segments:
                speech_row = copy.deepcopy(output_row)
                speech_row['start_time'] = segment.get("start")
                speech_row['end_time'] = segment.get("end")
                speech_row['sentence'] = segment.get("text")
                output_rows.append(speech_row)
        except Exception as error_message:
            logger.error("error={}".format(error_message))
            output_row['error'] = "{}".format(error_message)
            output_rows.append(output_row)

    output_dataframe = pandas.DataFrame(output_rows)
    output_A_datasets[0].write_with_schema(output_dataframe)
