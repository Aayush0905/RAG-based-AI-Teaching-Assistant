# how to user this RAG AI Teaching assistant on your own data
## step 1- collect your vedios
move all your video files to the videos folder

## step2 - convert to mp3
convert all the vedio files to mp3 by running video to mp3

## step3- conver np3 to json
convert all the mp3 files to json by running mp3 to json

## step4- convert the json files to vectors
use the file preprocess_json to convert the json files to a dataframe with Embeddings and save it as a joblib pickle

## step-5 prompt gereration and feeding to LLM
Read the joblib file and load it into the memory. Then create a relevant prompt as per the user query and feed it to the LLM