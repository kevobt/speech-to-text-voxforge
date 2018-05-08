import os
import json
import argparse

from typing import List


def read_prompt_file(speaker_directory) -> List[str]:
    """
    :param speaker_directory: a directory containing the transcriptions for the audio files
    :return: a list containing the transcription for each audio file
    """
    try:
        with open(os.path.join(speaker_directory, 'etc', 'PROMPTS')) as file:
            return file.readlines()
    except FileNotFoundError as ex:
        raise FileNotFoundError('"%s" has no PROMTS file' % os.path.abspath(speaker_directory))


def generate_json_file(source: str, destination: str):
    """
    :param source:
    :param destination:
    :return:
    """
    if not os.path.isdir(source):
        raise FileNotFoundError('The corpus directory "%s" does not exist' % os.path.abspath(source))

    speaker_directories = os.listdir(source)
    data = []

    for i, speaker_directory in enumerate(speaker_directories):
        print('Processing folder %s / %s' % (i + 1, len(speaker_directories)))

        # get the prompt file from the speaker directory
        try:
            prompt_file = read_prompt_file(os.path.join(source, speaker_directory))
        except FileNotFoundError as ex:
            print(ex)
            continue

        for row in prompt_file:
            try:
                # recreate the path to the audio file
                path = row.split(' ')[0]
                path = path.replace('/mfc/', '/wav/')
                path += '.wav'
                path = os.path.join(source, path)
                path = os.path.abspath(path)

                # get transcription from prompt file
                transcription = row.split(' ')[1:]
                transcription = ' '.join(transcription).replace('\n', '').lower()
                transcription = transcription.replace('-', '')

                # determine the size of audio file
                size = os.path.getsize(path)

                data.append({
                    'path': path,
                    'text': transcription,
                    'size': size
                })

            except Exception as ex:
                print(ex)

    # save training data to file
    with open(destination, 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tool for preparing training data from the Voxforge corpus")
    parser.add_argument('source', help='directory of the corpus')
    parser.add_argument('destination', help='path of the new (json) file containing the training data')
    args = parser.parse_args()

    generate_json_file(args.source, args.destination)
