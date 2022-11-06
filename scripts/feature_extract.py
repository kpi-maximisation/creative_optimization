from typing import Tuple
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from os import path
from subprocess import Popen, call
import subprocess
import pyautogui
import ffmpeg
import signal
import os
import re
import pandas as pd

from PIL import Image
from pytesseract import pytesseract
from log_supp import App_Logger


#     try:
#         self.logger.info('...')
#
#     except Exception:
#         self.logger.exception(
#             'Failed to ...')
#         sys.exit(1)

def get_instruction(image_path: str):
    path_to_tesseract = r"/usr/bin/tesseract"
    img = Image.open(image_path)
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(img).lower()

    if 'tap' in text:
        return 'tap'
    elif 'swipe l' in text:
        return 'swipe left'
    elif 'swipe r' in text:
        return 'swipe right'
    elif 'swipe u' in text:
        return 'swipe up'
    elif 'swipe do' in text:
        return 'swipe down'
    elif 'swipe' in text:
        return 'swipe'
    else:
        return 'tap_try'


class creativeFrameExtractor:
    '''
    class responsible for Extracting Creative Start and End Frames. It requires a chrome webdriver compatible with 
    selenium to be installed/ included in the run environment path.
    '''

    def __init__(self, preview_url: str,
                 save_location: str = '',
                 browser_edges: Tuple[float, float] = (70, 1039)) -> None:
        self.preview_url = preview_url
        self.start_time = time.time()
        self.engaged = False
        self.engagement_type = 'tap'
        self.browser_edges = browser_edges
        self.file_name = '-'.join(preview_url.split('/')[-3:-1])
        self.save_location = save_location
        self.video_name = path.join(self.save_location, self.file_name)
        self.cmd = f" ffmpeg -f alsa -ac 2 -i pulse -video_size 1920x1080 -framerate 60 -f x11grab -i :1 -c:v libx264rgb -qp 0 -preset ultrafast {self.video_name}.mkv -y"
        self.logger = App_Logger(
            "../logs/feature_extractor.log").get_app_logger()

        # Config

        # Browser config
        # Browser Options
        self.opt = Options()
        self.opt.add_argument("--hide-scrollbars")
        self.opt.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        # Browser logs
        self.capabilities = DesiredCapabilities.CHROME
        self.capabilities["goog:loggingPrefs"] = {"browser": "ALL"}

    def is_status_complete(self, passed_driver) -> bool:
        '''
        Function to check if the Ad-Unit is complete
        '''
        # Retrieve logs from the browser
        logs = passed_driver.get_log("browser")

        for log in logs:
            print(log['timestamp'])
            # select logs coming from Ad-Unit
            if log["source"] == "console-api":
                # Extract message from log
                message = log["message"].lower()

                if '"GAME CREATED"'.lower() in message or '"DROPPED"'.lower() in message:
                    # Start recording Game
                    print("Starting Recording Ad-Unit...")
                    return False

                if '"START"'.lower() in message:
                    # Engaged
                    print("Ad-UNIT Engaged...")

                    return False

                if '"GAME COMPLETE"'.lower() in message or ('"clickthrough"' in message) or ('"postwin"' in message):
                    # or '"video-top-ENDED"'.lower() in message or '"win"'.lower() in message
                    # Stop Recording Game
                    print("Stopped Recording Ad-Unit...")
                    print(log)
                    return True
        return False

    @staticmethod
    def terminate(process: call) -> None:  # call[bytes]
        '''
        Function to terminate a process
        '''
        # Video recording process terminator
        if process.poll() is None:
            call("kill -6 " + str(process.pid),
                 stdin=subprocess.PIPE, shell=True)

    @staticmethod
    def crop_video(filename: str, x_pos: float = 0, y_pos: float = 200, width: float = 650, height: float = 900) -> None:
        '''
        Function to crop a video with a location and size parameters
        '''
        print(filename)
        input_video = ffmpeg.input(f"{filename}.mkv")
        cropped_video = ffmpeg.crop(input_video, x_pos, y_pos, width, height)
        output_video = ffmpeg.output(cropped_video, f"{filename}_cropped.mkv")
        ffmpeg.run(output_video)

    @staticmethod
    def get_audio(filename: str):
        cmd_get_audio = f" ffmpeg -i {filename}.mkv -q:a 0 -map a {filename}.mp3 -y"
        fetch_audio = Popen(cmd_get_audio, stdout=subprocess.PIPE,
                            shell=True, preexec_fn=os.setsid)
        exitcode = fetch_audio.wait()

    def _imitate_engagement(self, ad_size: Tuple[float, float]) -> None:
        '''
        Function to imitate a given engagement type.
        '''
        center = (ad_size[0]/2, self.browser_edges[0]+(ad_size[1]/2))

        if self.engagement_type == "tap":
            pyautogui.moveTo(center[0], center[1], duration=1)
            pyautogui.leftClick()
        elif self.engagement_type == "swipe right":
            pyautogui.moveTo(center[0], center[1], duration=1)
            pyautogui.dragRel(center[0], 0, duration=1)
        elif self.engagement_type == "swipe left" or self.engagement_type == 'swipe':
            pyautogui.moveTo(center[0], center[1], duration=1)
            pyautogui.dragRel(-center[0], 0, duration=1)
        elif self.engagement_type == "swipe down":
            pyautogui.moveTo(center[0], center[1], duration=1)
            pyautogui.dragRel(0, center[1], duration=1)
        elif self.engagement_type == "swipe up":
            pyautogui.moveTo(center[0], center[1], duration=1)
            pyautogui.dragRel(0, -center[1], duration=1)
        elif self.engagement_type == "tap and hold":
            pyautogui.moveTo(center[0], center[1], duration=1)
            pyautogui.click()
        elif self.engagement_type == "scrub":
            pyautogui.moveTo(center[0] - (1/2 * center[0]),
                             center[1] - (2/3 * center[1]), duration=0.2)

            pyautogui.dragRel(center[0], 0, duration=0.2)
            pyautogui.dragRel(-center[0], (1/3 * center[1]), duration=0.2)
            pyautogui.dragRel(center[0], 0, duration=0.2)
            pyautogui.dragRel(-center[0], (1/3 * center[1]), duration=0.2)
            pyautogui.dragRel(center[0], 0, duration=0.2)

    def generate_preview_video(self, links: list, bad: list) -> None:
        '''
        Function to generate preview video and also a cropped version of the video
        '''
        # initialize selenium webDriver
        driver = webdriver.Chrome("/usr/bin/chromedriver",
                                  options=self.opt, desired_capabilities=self.capabilities)
        # maximize webdriver's window to maximize size
        driver.maximize_window()
        # get the starting frame
        url_not_working = []
        links = list(set(links) -set(bad))
        
        # processed = []
        for link in links:

            # get game id
            file_name = '-'.join(link.split('/')[-3:-2])
            print("Filename: ", file_name)

            try:
                # Load Ad-Unit through selenium
                driver.get(link)

                # Locate Ad-Unit Element from Browser
                canvas = driver.find_element(By.TAG_NAME, "canvas")

                # Capture start frame
                canvas.screenshot(
                    path.join(
                        '../start_frame/',  f'{file_name}_start_frame.png')
                )
                self.logger.info(
                    f'start frame extracted for game id: {file_name}')
                sleep(2)
            except TimeoutException:
                print("TimeoutException Throwed")
                self.logger.info(
                    f'Ad-Unit Status console logs did not complete. Engagement Failed. for game id: {file_name}')
                print("Ad-Unit Status console logs did not complete. Engagement Failed.")
                url_not_working.append(link)
                with open("./url_not_working.csv", "a") as myfile:
                    myfile.write(link + '\n')
                continue
                # driver.close()

            except NoSuchElementException:
                print(f"Ad-Unit Failed to load: {file_name}")
                self.logger.info(
                    f'Ad-Unit Failed to load for game id: {file_name}')
                with open("./url_not_working.csv", "a") as myfile:
                    myfile.write(link + '\n')
                url_not_working.append(link)
                continue

            # record the video
            try:
                # get engagement type
                self.engagement_type = get_instruction(
                    '../start_frame/' + f'{file_name}_start_frame.png')

                print("Engagement Chosen:" + self.engagement_type)
                self.logger.info(
                    f'Engagement type {self.engagement_type} chosen for game id: {file_name}')

                # locate Ad-Unit element from browser

                # canvas = driver.find_element(By.TAG_NAME, "canvas")

                cmd = f" ffmpeg -hide_banner -loglevel error -f alsa -ac 2 -i pulse -video_size 1920x1080 -framerate 60 -f x11grab -i :1 -c:v libx264rgb -qp 0 -preset ultrafast ../video/{file_name}.mkv -y"

                # start recording the entire screen
                video_recording = Popen(
                    cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

                canvas = driver.find_element(By.TAG_NAME, "canvas")

                # Identify the size of Ad-Unit
                ad_size = (canvas.size.get("width"), canvas.size.get("height"))

                # Engage Ad Unite
                self._imitate_engagement(ad_size)

                self.start_time = time.time()

                # Continuously check Status of Ad-Unit using it's console log
                # or (time.time() - self.start_time) > 60
                WebDriverWait(driver, 30).until(
                    self.is_status_complete or (time.time() - self.start_time) > 30)

                print(f"Elapsed time:{time.time() - self.start_time}")
                sleep(2)

                # stop video recording
                os.killpg(os.getpgid(video_recording.pid), signal.SIGTERM)

                stop_ffmpeg = "pkill ffmpeg"
                manual_ffmpeg_stop = Popen(
                    stop_ffmpeg, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
                manual_ffmpeg_stop.wait()

                # take screenshots
                canvas.screenshot(
                    path.join(
                        '../end_frame/' + f'{file_name}_end_frame.png')
                )
                print('End frame Captured')

                # crop Generated Preview video recording
                # self.crop_video(self.video_name, x_pos=0, y_pos=70,
                #                 width=ad_size[0], height=ad_size[1])

                # get audio
                # self.get_audio(self.video_name)

                with open("./processed.csv", "a") as myfile:
                    myfile.write(link + "\n")
            except TimeoutException:
                print("TimeoutException Throwed")
                print("Ad-Unit Status console logs did not complete. Engagement Failed.")
                url_not_working.append(link)
                self.logger.info(
                    f'Ad-Unit Status console logs did not complete. Engagement Failed. for game id: {file_name}')
                with open("./url_not_working.csv", "a") as myfile:
                    myfile.write(link + '\n')
            except NoSuchElementException:
                print(f"Ad-Unit Failed to load: {self.preview_url}")
                url_not_working.append(link)
                self.logger.info(
                    f'Ad-Unit failed to load for game id: {file_name}')
                with open("./url_not_working.csv", "a") as myfile:
                    myfile.write(link + '\n')
        driver.close()
        
        

    def generate_start_frame(self) -> None:
        '''
        function to generate creative start and end frames.
        '''
        # Initialize selenium driver
        driver = webdriver.Chrome(
            options=self.opt, desired_capabilities=self.capabilities,
        )

        # Maximize webdriver window for maximum resolution
        driver.maximize_window()

        try:
            # Load Ad-Unit through selenium
            driver.get(self.preview_url)

            # Locate Ad-Unit Element from Browser
            canvas = driver.find_element(By.TAG_NAME, "canvas")

            # Capture start frame
            canvas.screenshot(
                path.join(self.save_location,
                          f'{self.file_name}_start_frame.png')
            )
            print('Start frame Captured')

            #

            # close the selenium browser window
            driver.close()
        except TimeoutException:
            print("TimeoutException Throwed")
            print("Ad-Unit Status console logs did not complete. Engagement Failed.")
            driver.close()

        except NoSuchElementException:
            print(f"Ad-Unit Failed to load:{self.preview_url}")
            driver.close()

    def generate_frames(self) -> None:
        '''
        function to generate creative start and end frames.
        '''
        # Initialize selenium driver
        driver = webdriver.Chrome(
            options=self.opt, desired_capabilities=self.capabilities,
        )

        # Maximize webdriver window for maximum resolution
        driver.maximize_window()

        try:
            # Load Ad-Unit through selenium
            driver.get(self.preview_url)

            # Locate Ad-Unit Element from Browser
            canvas = driver.find_element(By.TAG_NAME, "canvas")

            # Capture start frame
            canvas.screenshot(
                path.join(self.save_location,
                          f'{self.file_name}_start_frame.png')
            )
            print('Start frame Captured')

            # Identify size of Ad-Unit
            ad_size = (canvas.size.get("width"), canvas.size.get("height"))

            # Engage Ad-Unit
            self._imitate_engagement(ad_size)

            # Continuously check Status of Ad-Unit using it's console log
            # until it reached a "GAME COMPLETE" Status
            WebDriverWait(driver, 30).until(
                self.is_status_complete or self.start_time < 30)

            sleep(5)

            # capture End frame
            canvas.screenshot(
                path.join(self.save_location,
                          f'{self.file_name}_end_frame.png')
            )
            print('End frame Captured')

            # close the selenium browser window
            driver.close()
        except TimeoutException:
            print("TimeoutException Throwed")
            print("Ad-Unit Status console logs did not complete. Engagement Failed.")
            driver.close()

        except NoSuchElementException:
            print(f"Ad-Unit Failed to load: {self.preview_url}")
            driver.close()


# use the script
url = "https://s3.us-west-1.amazonaws.com/a.futureadlabs.com-us-west-1-backup/us-west-1/games/adunit-lionsgate-spiral-puzzle-v2-mpu/47ab0df166aaa7d1650f/index.html"
ext = creativeFrameExtractor(url, save_location='./extracted/')
bad = pd.read_csv('./url_not_working.csv')
bad_url = bad.url_not_working
processed = pd.read_csv('./processed.csv')
link_processed = processed.processed

new_link = list(set(bad_url)) + list(set(link_processed))

df = pd.read_csv("../data/performance_data.csv")
links = df.preview_link
# links = ['https://s3.us-west-1.amazonaws.com/a.futureadlabs.com-us-west-1-backup/us-west-1/games/adunit-western-union-sensory-unit-swipe-right-tap-mpu/571dd7229502e37d0b08/index.html']

links = list(set(links) -set(new_link))
print(f'remaining: {len(links)}')
ext.generate_preview_video(links, bad_url)
