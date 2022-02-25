import cv2

from cv2 import imwrite as cv2_imwrite
from typing import BinaryIO, NoReturn, Callable
from pathlib import Path
from prefect import task
import typer


# Meta class for CAM data
class CamIO(BinaryIO):
    imwrite: Callable[[], NoReturn]
    release: Callable[[], None]
    isOpened: Callable[[], bool]
    get: Callable[[int], float]


@task
def mp4_to_jpg(video: str, output: str = "./data") -> bool:

    # file path in os format
    file = Path(video)

    # Checks existance of file or exits
    if not file.is_file():
        print("Error: reading file. Does it exists?")
        return False

    try:
        # creating a folder named dat
        Path(output).mkdir(parents=True, exist_ok=True)
    except OSError:
        # if not created then raise error
        print("Error: Creating directory of data")

    # Capture of video from opencv
    cam: CamIO = cv2.VideoCapture(str(file))

    # Settings time and time per frame variables
    time = 0
    time_per_frame = 0
    while True:
        # Reads image frame from camara IO
        success, image = cam.read()

        # Try to get frame number from cv2 properties
        frame = int(cam.get(cv2.CAP_PROP_POS_FRAMES))

        # Trying to get ms value from frame
        # The last frames dont have any time associated. We need to calculate
        if cam.get(cv2.CAP_PROP_POS_MSEC) == 0:
            time = time_per_frame * frame
        else:
            # Calculation of frame based on previous values
            time = cam.get(cv2.CAP_PROP_POS_MSEC)
            time_per_frame = time / frame
        if not success:
            break

        # Name of image frame
        name = f"{output}/{str(frame).zfill(4)}-{int(round(time, 0))}.jpg"

        # writing the extracted image
        cv2_imwrite(name, image)

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

    # Return link to task management
    return True


# Allows typer exection in termial environment
if __name__ == "__main__":
    typer.run(mp4_to_jpg.run)
