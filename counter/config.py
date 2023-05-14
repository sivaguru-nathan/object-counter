import os

from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo
from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from counter.domain.actions import CountDetectedObjects

tfs_host = os.environ.get('TFS_HOST', 'localhost')
tfs_port = os.environ.get('TFS_PORT', 8501)
mongo_host = os.environ.get('MONGO_HOST', 'localhost')
mongo_port = os.environ.get('MONGO_PORT', 27017)
mongo_db = os.environ.get('MONGO_DB', 'prod_counter')
model_name=os.environ.get('MODEL_NAME', 'saved_models')
mongo_username=os.environ.get('MONGO_USERNAME', 'admin')
mongo_password=os.environ.get('MONGO_PASSWORD', 'admin')
postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
postgres_port = os.environ.get('POSTGRES_PORT', 27017)
postgres_db = os.environ.get('POSTGRES_DB', 'prod_counter')
postgres_username=os.environ.get('POSTGRES_USERNAME', 'admin')
postgres_password=os.environ.get('POSTGRES_PASSWORD', 'admin')


def dev_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


def prod_count_action() -> CountDetectedObjects:
    
    return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, model_name),
                                CountMongoDBRepo(host=mongo_host, port=mongo_port, database=mongo_db, user_name=mongo_username,password=mongo_password))

def get_count_action() -> CountDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    count_action_fn = f"{env}_count_action"
    return globals()[count_action_fn]()
