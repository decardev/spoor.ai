from tasks import mp4_to_jpg, jpg_to_csv, csv_to_sqlite, sql_to_graph
from prefect import Flow, Parameter

with Flow("CAM-to-GRAPH") as flow:
    mp4_file = Parameter("mp4_file", default="./data/Pigeon - 6093.mp4")
    jpg_root = Parameter("jpg_root", default="./data/Pigeon-6093")
    csv_file = Parameter("csv_file", default="./data/Pigeon.csv")
    sql_file = Parameter("sql_file", default="./data/sqlite.db")
    out_root = Parameter("out_root", default="./data")

    link = mp4_to_jpg(mp4_file, jpg_root)
    link = jpg_to_csv(jpg_root, csv_file, link)
    link = csv_to_sqlite(csv_file, sql_file, link)
    link = sql_to_graph(sql_file, out_root, link)


if __name__ == "__main__":

    flow.run(  # type: ignore
        parameters={
            "mp4_file": "./data/Pigeon - 6093.mp4",
            "jpg_root": "./data/Pigeon-6093",
            "csv_file": "./data/Pigeon.csv",
            "sql_file": "./data/sqlite.db",
            "out_root": "./data",
        }
    )
