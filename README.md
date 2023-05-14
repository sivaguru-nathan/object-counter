# Machine Learning & Hexagonal Architecture

The goal of this repo is demonstrate how to apply Hexagonal Architecture in a ML based system 

The model used in this example has been taken from 
[IntelAI](https://github.com/IntelAI/models/blob/master/docs/object_detection/tensorflow_serving/Tutorial.md)


## Download the tf model
```
wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
rm rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
chmod -R 777 tmp/rfcn_resnet101_coco_2018_01_28
mkdir -p tmp/models/tf/rfcn/1
mv tmp/rfcn_resnet101_coco_2018_01_28/saved_model/saved_model.pb tmp/models/tf/rfcn/1
rm -rf tmp/rfcn_resnet101_coco_2018_01_28
```

## Download the torch model
```
wget https://download.pytorch.org/models/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth
wget https://raw.githubusercontent.com/pytorch/serve/master/examples/object_detector/fast-rcnn/model.py
mkdir -p tmp/models/torch/fasterrcnn
mv fasterrcnn_resnet50_fpn_coco-258fb6c6.pth tmp/models/torch/fasterrcnn/fasterrcnn.pth
mv model.py tmp/models/torch/fasterrcnn/fasterrcnn.py

```

## create model archieve file for torch model

```
torch-model-archiver --model-name fasterrcnn --version 1.0 --model-file tmp/models/torch/fasterrcnn/fasterrcnn.py --serialized-file tmp/models/torch/fasterrcnn/fasterrcnn.pth --handler object_detector
mv fasterrcnn.mar tmp/models/torch/fasterrcnn/
```


## Setup Environment Varibles

```
Configure environment variable in .env file. Available configurations are listed below

ENV="prod" # can able to switch between 'prod' and 'dev'
DB="postgres" # can able to switch between 'postgres' and 'mongo'
SERVER="torch" # can able to switch between 'torch' and 'tf'

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
TF_MODEL_NAME="rfcn"  
TF_OMP_NUM_THREADS=4 
TF_TENSORFLOW_INTER_OP_PARALLELISM=2  
TF_TENSORFLOW_INTRA_OP_PARALLELISM=4 
TF_MODEL_BASE_PATH="/models"
TF_LOCAL_MODEL_PATH="/C/Users/a_s_g/Videos/tasks/object-counter/tmp/models/tf"

#Torch serve configuration
PT_PORT=8080
PT_MODEL_NAME="fasterrcnn"  
PT_MODEL_BASE_PATH="/models"
PT_LOCAL_MODEL_PATH="/C/Users/a_s_g/Videos/tasks/object-counter/tmp/models/torch"
PT_CONFIG="/models/config.properties"
```


## Build Docker Image

```
docker-compose build
```


## Run the application
```
docker-compose up
```

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
