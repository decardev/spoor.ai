import sqlite3
from pandas import read_csv as pandas_read_csv
from prefect import task
import typer

# This could be implemented with peewee or sqlalchemy to improve performance and query
# from peewee import SqliteDatabase, Model, CharField, TimestampField, IntegerField, FloatField  # type: ignore

# db = SqliteDatabase("sqlite.db")

# class Person(Model):
#     name = CharField()
#     timestamp = TimestampField()
#     frame = IntegerField()
#     xmin = FloatField()
#     ymin = FloatField()
#     xmax = FloatField()
#     ymax = FloatField()
#     confidence = FloatField()

#     class Meta:
#         database = db


@task
def csv_to_sqlite(file: str, db: str = "./data/sqlite.db", link: bool = True) -> bool:
    try:
        # load data
        df = pandas_read_csv(file)
        # strip whitespace from headers
        df.columns = df.columns.str.strip()

        con = sqlite3.connect(db)

        # drop data into database
        df.to_sql("detection", con, if_exists="replace", index=False)  # type: ignore
        con.close()
        return True
    except:
        return False


# Allows typer exection in termial environment
if __name__ == "__main__":
    typer.run(csv_to_sqlite.run)
