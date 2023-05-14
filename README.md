# Machine Learning & Hexagonal Architecture

The goal of this repo is demonstrate how to apply Hexagonal Architecture in a ML based system 

The model used in this example has been taken from 
[IntelAI](https://github.com/IntelAI/models/blob/master/docs/object_detection/tensorflow_serving/Tutorial.md)


## Download the model
```
wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
rm rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
chmod -R 777 tmp/rfcn_resnet101_coco_2018_01_28
mkdir -p tmp/model/rfcn/1
mv tmp/rfcn_resnet101_coco_2018_01_28/saved_model/saved_model.pb tmp/model/rfcn/1
rm -rf tmp/rfcn_resnet101_coco_2018_01_28
```


## Setup Environment Varibles

```
Configure environment variable in .env file. Available configurations are listed below

#Mongodb Configurations
MONGO_PORT=27017
MONGO_DB='prod_counter'
MONGO_USERNAME='admin'
MONGO_PASSWORD='admin'

#Postgres Configurations
POSTGRES_PORT=5432
POSTGRES_USER='admin'
POSTGRES_PASSWORD='admin'
POSTGRES_DB='prod_counter'

#Tf serve configrations
TFS_PORT=8501
MODEL_NAME="rfcn"  
OMP_NUM_THREADS=4 
TENSORFLOW_INTER_OP_PARALLELISM=2  
TENSORFLOW_INTRA_OP_PARALLELISM=4 
MODEL_BASE_PATH="/models"

#Model File Path Configurations
LOCAL_MODEL_PATH="/C/Users/a_s_g/Videos/tasks/object-counter/tmp/models"
```


## Build Docker Image

```
docker-compose build
```


## Run the application
docker-compose up

## Call the service

```shell script
 curl -F "threshold=0.9" -F "file=@resources/images/boy.jpg" http://0.0.0.0:5000/object-count
 curl -F "threshold=0.9" -F "file=@resources/images/cat.jpg" http://0.0.0.0:5000/object-count
 curl -F "threshold=0.9" -F "file=@resources/images/food.jpg" http://0.0.0.0:5000/object-count
```

## Run the tests

```
pytest

```
