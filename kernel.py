from skimage.metrics import structural_similarity as ssim
from pytubefix import YouTube
from pytubefix.cli import on_progress
from colorama import init, Fore
import cv2

import json
import shutil
import os

def UpdateLists(prediction, url, datafile="links.json"):
      with open(datafile, "r") as file:
            data = json.load(file)

      print(Fore.LIGHTMAGENTA_EX + "\nHas the model yielded correct prediction?")
      feedback = input(Fore.LIGHTMAGENTA_EX + "Enter y/n for yes/no: ").lower()

      if feedback not in ("y", "n", "yes", "no"):
            print(Fore.RED + "\nError: Invalid Feedback\n")
            return

      with open(datafile, "w") as file:
            blacklist, whitelist = data["blacklist"], data["whitelist"]

            if (prediction and (feedback == "y" or "yes")) or (not prediction and (feedback == "n" or "no")):
                  whitelist.remove(url) if url in whitelist else None
                  blacklist.append(url) if url not in blacklist else None
            elif (prediction and (feedback == "n" or "no")) or (not prediction and (feedback == "y" or "yes")):
                  blacklist.remove(url) if url in blacklist else None
                  whitelist.append(url) if url not in whitelist else None

            json.dump(data, file, indent=4)
            
      print(Fore.LIGHTMAGENTA_EX + "\nEvery single feedback counts in improving this model! Thank you!\n")

def CompareFrames(link):
      fc = 2
      ic = 0
      rrf = 0
      print(Fore.LIGHTGREEN_EX + "Analyzation of Frames in Process...\n")

      while (fc < 185):
            frame = f"./Frames/{fc}.jpg"
            dependency = f"./Dependencies/{ic}.jpg"

            if not os.path.exists(frame) or not os.path.exists(dependency):
                  print(Fore.YELLOW + "NO RICKROLL DETECTED!\n")
                  UpdateLists(False, link)
                  break

            i1 = cv2.imread(frame)
            i2 = cv2.imread(dependency)

            if i2 is not None:
                  if i1.shape != i2.shape:
                        i2 = cv2.resize(i2, (i1.shape[1], i1.shape[0]))
                  
                  g1 = cv2.cvtColor(i1, cv2.COLOR_BGR2GRAY)
                  g2 = cv2.cvtColor(i2, cv2.COLOR_BGR2GRAY)

                  score, _ = ssim(g1, g2, full=True)
                  
                  if score < 0.6:
                        fc += 1
                        ic += 6
                        continue
                  else:
                        rrf += 1
                        fc += 1
                        ic += 6

                        if (rrf >= 10):
                              print(Fore.YELLOW + f"THERE IS A RICKROLL! (More than 15 Frames Detected.)\n")
                              UpdateLists(True, link)
                              break
                        else:
                              continue

            else:
                  print(Fore.YELLOW + "NO RICKROLL DETECTED!\n")
                  UpdateLists(False, link)
                  break

      else:
            print(Fore.YELLOW + "NO RICKROLL DETECTED!\n")
            UpdateLists(False, link)

      shutil.rmtree("./Dependencies")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    percentage = (1 - bytes_remaining / total_size) * 100
    bar = f" ↳ |{'█' * int(percentage):<50}| {percentage:.1f}%"
    
    print(Fore.LIGHTGREEN_EX + bar, end="\r")
           
def ExtractFramesFromURL(link):
      forbidden_chars = ('/', '\\', '*', '?', ':', '<', '>', '|', '"')
      valid_title = ''
      os.mkdir('./Dependencies') if not os.path.exists('./Dependencies') else None

      try:
            print()
            yt = YouTube(link, on_progress_callback = on_progress)
            ys = yt.streams.get_highest_resolution()
            ys.download(output_path="./")
            print(Fore.LIGHTGREEN_EX + "\n\nVideo Download Successful")

            valid_title = ''.join(char for char in yt.title if char not in forbidden_chars)
            vidcap = cv2.VideoCapture(f"./{valid_title}.mp4")
            count = 0

            success, image = vidcap.read()
            while success:
                  if image is not None:
                        cv2.imwrite(f"./Dependencies/{count}.jpg", image)
                        count += 1

                  success, image = vidcap.read()

            vidcap.release()
            cv2.destroyAllWindows()
      
            os.remove(f"./{valid_title}.mp4")
            CompareFrames(link)

      except:
            print(Fore.RED + "Error: Either youtube hyperlink is invalid or video is unavailable\n")
            return

      finally:
            os.remove(f"./{valid_title}.mp4") if (valid_title and os.path.exists(f"./{valid_title}.mp4")) else None
            shutil.rmtree("./Dependencies") if os.path.exists("./Dependencies") else None

def VerifyLists(link, datafile="links.json"):
      with open(datafile, "r") as file:
            data = json.load(file)

            if link in data["blacklist"]:
                  print(Fore.YELLOW + "\nRICKROLL DETECTED! This link has been blacklisted previously.\n")
                  UpdateLists(True, link)
            elif link in data["whitelist"]:
                  print(Fore.YELLOW + "\nLINK IS SAFE! This link has been previously tested negative.\n")
                  UpdateLists(False, link)
            else:
                  ExtractFramesFromURL(link)

def main():
      init(autoreset=True)
      
      print(Fore.LIGHTCYAN_EX + "\nIs Rick Inside?")
      print(Fore.LIGHTCYAN_EX + "By ADITYA VN KADIYALA")

      while True:
            url = input(Fore.LIGHTGREEN_EX + "\nEnter URL: ")
            VerifyLists(url)

if __name__ == "__main__":
      main()
