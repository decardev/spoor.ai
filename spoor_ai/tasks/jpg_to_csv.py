from torch.hub import load as torch_load
from typing import Callable, Any
from glob import glob
from pathlib import Path
from typing import List
from prefect import task
import typer
import gc

# Columns to display on csv
COLUMNS = ["name", "timestamp", "frame", "xmin", "ymin", "xmax", "ymax", "confidence"]

# Max number of elemnets to read in torch model. Limited by memory.
MAX_PER_EVAL = 10


# Creates agroupation of list based on interval
def gr_max(list: List[Any]) -> List[List[Any]]:
    return [list[n : n + MAX_PER_EVAL] for n in range(0, len(list), MAX_PER_EVAL)]


@task
def jpg_to_csv(path: str, output: str = "./data/data.csv", link: bool = True) -> bool:

    # Loading of model
    model: Callable[[Any], Any] = torch_load("yolov3", "yolov3", source="local")

    # Loading of images files
    images = [Path(f) for f in glob(f"{path}/*.jpg")]

    # Calculation of frame from image name
    frame: List[List[str]] = gr_max([f.stem.split("-")[0] for f in images])

    # Calculation of time from image name
    time: List[List[str]] = gr_max([f.stem.split("-")[1] for f in images])

    # Opening file
    with open(output, "w+") as f:
        for gr, images_group in enumerate(gr_max(images)):
            # Application of model in image group
            results = model(images_group)
            for ind, df in enumerate(results.pandas().xyxyn):

                # Creation of df for such group and adding new columns
                df = df.assign(frame=frame[gr][ind], timestamp=time[gr][ind])

                # Save to csv
                df.to_csv(
                    f,
                    header=(gr == 0) and (ind == 0),
                    index=False,
                    line_terminator="\n",
                    columns=COLUMNS,
                )

            # This should be assesed to understand if there is a memory leak during executing. Its a trade off in the speed.
            del results, df
            gc.collect()

    # Output true to create link between taskss
    return True


# Allows typer exection in termial environment
if __name__ == "__main__":
    typer.run(jpg_to_csv.run)
