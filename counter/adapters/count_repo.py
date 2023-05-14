from typing import List

from pymongo import MongoClient
import psycopg2

from counter.domain.models import ObjectCount
from counter.domain.ports import ObjectCountRepo

class CountInMemoryRepo(ObjectCountRepo):

    def __init__(self):
        self.store = dict()

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        if object_classes is None:
            return list(self.store.values())

        return [self.store.get(object_class) for object_class in object_classes]

    def update_values(self, new_values: List[ObjectCount]):
        for new_object_count in new_values:
            key = new_object_count.object_class
            try:
                stored_object_count = self.store[key]
                self.store[key] = ObjectCount(key, stored_object_count.count + new_object_count.count)
            except KeyError:
                self.store[key] = ObjectCount(key, new_object_count.count)
        print("-----------------store details-------------\n",self.store)


class CountMongoDBRepo(ObjectCountRepo):

    def __init__(self, host, port, database,user_name,password):
        self.__host = host
        self.__port = port
        self.__database = database
        self.__username=user_name
        self.__password=password
        

    def __get_counter_col(self):
        url=f'mongodb://{self.__username}:{self.__password}@{self.__host}:{self.__port}'
        client = MongoClient(url)

        db = client[self.__database]
        counter_col = db.counter
        return counter_col

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        counter_col = self.__get_counter_col()
        query = {"object_class": {"$in": object_classes}} if object_classes else None
        counters = counter_col.find(query)
        object_counts = []
        for counter in counters:
            object_counts.append(ObjectCount(counter['object_class'], counter['count']))
        return object_counts

    def update_values(self, new_values: List[ObjectCount]):
        counter_col = self.__get_counter_col()
        for value in new_values:
            counter_col.update_one({'object_class': value.object_class}, {'$inc': {'count': value.count}}, upsert=True)




class CountPostgresRepo(ObjectCountRepo):
    def __init__(self,host, port, database,user_name,password):
        
        self.db_connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user_name,
            password=password
        )
        with self.db_connection:
            with self.db_connection.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS object_counts (
                        object_class VARCHAR(255) PRIMARY KEY,
                        count INTEGER NOT NULL
                    )""")
    
    def __del__(self):
        self.db_connection.close()
    
    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        with self.db_connection:
            with self.db_connection.cursor() as cur:
                if object_classes:
                    cur.execute("SELECT object_class, count FROM object_counts WHERE object_class IN %s", (tuple(object_classes),))
                else:
                    cur.execute("SELECT object_class, count FROM object_counts")
                rows = cur.fetchall()
        object_counts=[]
        for object_class, count in rows:
             object_counts.append(ObjectCount(object_class, count))
        return object_counts


    def update_values(self, new_values: List[ObjectCount]):
        for value in new_values:
            with self.db_connection:
                with self.db_connection.cursor() as cur:
                    cur.execute("SELECT count FROM object_counts WHERE object_class = %s", (value.object_class,))
                    row = cur.fetchone()
                    if row:
                        cur.execute("UPDATE object_counts SET count = count + %s WHERE object_class = %s", (value.count, value.object_class))
                    else:
                        cur.execute("INSERT INTO object_counts (object_class, count) VALUES (%s, %s)", (value.object_class, value.count))
