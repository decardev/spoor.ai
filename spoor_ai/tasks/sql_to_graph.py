import matplotlib.pyplot as plt

from peewee import SqliteDatabase, Model, CharField, IntegerField, FloatField  # type: ignore
from peewee import fn  # type: ignore
from peewee import Function as _Function  # type: ignore
from typing import Any, List
import itertools
from prefect import task
from statistics import median_high
import typer


@task
def sql_to_graph(database: str, output: str = "./data", link: bool = True) -> bool:
    db = SqliteDatabase(database)

    # peewee ORM class for accessing sql
    class Detection(Model):
        name = CharField()
        timestamp = IntegerField()
        frame = IntegerField()
        xmin = FloatField()
        ymin = FloatField()
        xmax = FloatField()
        ymax = FloatField()
        confidence = FloatField()

        # database connection and primary key instance
        class Meta:
            database = db
            primary_key = False  # Pandas does not create primary key

    # Cnecting and creating table if does not exists
    db.connect()
    db.create_tables([Detection], safe=True)  # type: ignore
    db.close()

    # Query and agroupation based on birds, timestamp and count
    query: Any = (
        Detection.select(Detection.timestamp, fn.COUNT(Detection.name).alias("count"), Detection.confidence)  # type: ignore
        .where(Detection.name == "bird")  # type: ignore
        .group_by(Detection.timestamp)  # type: ignore
        .order_by(Detection.timestamp)  # type: ignore
    )

    # Creatino of data list
    ans = [[q.timestamp, q.count, q.confidence] for q in query]

    # Grouping based on miliseconds
    timestamp = [q.timestamp for q in query]
    ms_count = [q.count for q in query]

    # Grouping based on seconds and not mili seconds
    sec_count: List[int] = []
    for _, min_count_list in itertools.groupby(ans, lambda x: x[0] // 1000):
        sec_count.append(median_high([x[1] for x in min_count_list]))

    # Grouping based on seconds and confidence weight
    sec_count_confidence: List[float] = []
    for _, min_count_list in itertools.groupby(ans, lambda x: x[0] // 1000):
        sec_count_confidence.append(median_high([x[1] * x[2] for x in min_count_list]))

    # Miliseconds image with birds detection
    plt.figure()
    plt.xlabel("Duration video (mili seconds)")  # type: ignore
    plt.ylabel("Number of birds detected")  # type: ignore
    plt.plot(timestamp, ms_count)
    plt.savefig(f"{output}/graph_ms.jpg")

    # Seconds image with birds detection
    plt.figure()
    plt.plot(sec_count)
    plt.xlabel("Duration video (seconds)")  # type: ignore
    plt.ylabel("Number of birds detected")  # type: ignore
    plt.savefig(f"{output}/graph_sec.jpg")

    # Seconds image with birds detection in confidence
    plt.figure()
    plt.plot(sec_count_confidence)
    plt.xlabel("Duration video (seconds)")  # type: ignore
    plt.ylabel("Number of confidence birds")  # type: ignore
    plt.savefig(f"{output}/graph_conf_sec.jpg")

    return True


# Allows typer exection in termial environment
if __name__ == "__main__":
    typer.run(sql_to_graph.run)
    #Random modification
