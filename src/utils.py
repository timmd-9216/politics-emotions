from pytube import YouTube
import os

def download_video_from_youtube(url: str, output_file: str) -> None:
    # función que permite la descarga de un video a partir de su url.
    video_caller = YouTube(url)
    print(video_caller.title)
    video = video_caller.streams.filter(only_audio=False, only_video=False, resolution="720p").first()
    out_path = video.download()
    os.rename(out_path, output_file)
    print("Done!!")
    
    
import gdown

def download_video_from_drive(file_id: str, output_file: str) -> None:
    #file_id = "1H3CDjjv6uUaEg3glmSDc7ZHO8oXy15To"  # Replace this with your file's ID
    #output_file = "video_sample.mp4"  # Replace "data_file.ext" with the desired output filename and extension

    gdown.download(f"https://drive.google.com/uc?id={file_id}", output_file)
    print("Done!!")
    
    
import cv2
import matplotlib.pyplot as plt

class VideoContainer():
    # Falta sumar el release de los objetos -> Ver CV2

    def __init__(self, video_path: str):
        self.video = cv2.VideoCapture(video_path, )
        self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.duration = self.get_duration()
        self.actual_frame_id = 0

    def get_duration(self):
        # Admite videos de menos de 1 hora.
        mins = int(self.total_frames / self.fps // 60)
        secs = ((self.total_frames / self.fps / 60) - mins)
        secs = int(secs * 60)
        return (mins, secs)

    def get_duration_formated(self):
        return f'{self.duration[0]}:{self.duration[1]}'

    def get_summary(self):
        print(f"Total frames = {self.total_frames}")
        print(f"FPS = {self.fps}")
        print(f"Width = {self.width}")
        print(f"Height = {self.height}")
        print(f"Duration = {self.get_duration_formated()}")

    def set_actual_frame(self, frame_id: int):
        self.actual_frame_id = frame_id
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.actual_frame_id)

    def get_actual_frame_id(self):
        return self.actual_frame_id #video.get(cv2.CAP_PROP_POS_FRAMES)

    def get_actual_frame_array(self, color_code: str | None = None) :
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.actual_frame_id)
        _, f_array = self.video.read()
        f_array = self.change_frame_color(f_array, color_code)
        return f_array

    def get_actual_frame(self):
        return (self.get_actual_frame_id(), self.get_actual_frame_array())

    def show_actual_frame(self):
        f = self.get_actual_frame_array()
        f = self.change_frame_color(f, "RGB")
        plt.axis("off")
        plt.imshow(f)
        plt.show()

    # def set_frame_color(self, color_code: str):
    #     if color_code not in ["BGR", "RGB", "GRAY"]:
    #         raise ValueError("Color code must be one of RGB or GRAY")

    #     if self.frame_color == "BGR" and color_code == "RGB":
    #         self.change_color_function

    #     self.frame_color = color_code

    def change_frame_color(self, frame, color_code):
        if color_code not in [None, "RGB", "GRAY"]:
           raise ValueError("Color code must be one of RGB or GRAY")

        if color_code == "RGB":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        elif color_code == "GRAY":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return frame

    def save_clip(self, filepath, start_frame, end_frame):

        # Set the video writer
        w = int(self.width)
        h = int(self.height)
        start_frame = int(start_frame)
        end_frame = int(end_frame)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can change the codec as needed
        out = cv2.VideoWriter(filepath, fourcc, self.fps, (w, h))
        self.set_actual_frame(start_frame)

        # Read and write frames to the output video
        for frame_number in range(start_frame, end_frame):
            ret, frame = self.video.read()
            if not ret:
                break

            # Write the frame to the output video
            out.write(frame)

        out.release()






# plt.axis("off")
# plt.imshow(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))
# plt.show()