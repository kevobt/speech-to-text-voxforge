# speech-to-text-voxforge

## Download the speech corpus
In order to download the speech corpus run

```shell
python downloader.py "voxforge-corpus"
```

You can additionally specify the amount of speaker directories to be downloaded using `-n` or the amount of threads to be used for the download using `-w`:

```shell
python downloader.py "voxforge-corpus" -n 20000 -w 15
```

## Generate training data
If you want to generate a training data file for the [speech recognition tool](https://github.com/KevNetG/speech-to-text), run `generator.py` providing the path to the directory where the voxforge corpus was being downloaded and a path to the new file where the training data should be stored. The data will be stored as JSON.

```shell
python generator.py "voxforge-corpus" "training_data.json"
```
