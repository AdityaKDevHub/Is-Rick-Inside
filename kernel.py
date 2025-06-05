from skimage.metrics import structural_similarity as ssim
from pytubefix import YouTube
from pytubefix.cli import on_progress
from customtkinter import *
import cv2
from PIL import Image

import json
import shutil
import os
import threading

app = CTk()
app.title("Is Rick Inside?")
width, height = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry(f"{width}x{height}+0+0")
set_appearance_mode("dark")

frame = CTkFrame(master=app, fg_color="transparent")
frame.pack(expand=True, fill="both")

urlinput = CTkEntry(master=app, placeholder_text="Enter YouTube hyperlink...", width=900)
urlinput.place(relx=0.45, rely=0.2, anchor="center")

submiturl = CTkButton(master=app, text="Sumbit for Analysis", fg_color="transparent",
                  hover_color="#4d004d", command=lambda: VerifyLists(urlinput.get()), border_width=2)
submiturl.place(relx=0.87, rely=0.2, anchor="center")

alert = CTkLabel(master=frame, text="", font=("Arial", 20))
alert.place(relx=0.5, rely=0.3, anchor="center")

imgcount = 2

ytimg_label = CTkLabel(master=frame, text="")
ytimg_label.place(relx=0.2, rely=0.4, anchor="center")
ar1label = CTkLabel(master=frame, text="")
ar1label.place(relx=0.35, rely=0.45, anchor="center")
grlabel = CTkLabel(master=frame, text="")
grlabel.place(relx=0.47, rely=0.6, anchor="center")
ar2label = CTkLabel(master=frame, text="")
ar2label.place(relx=0.63, rely=0.68, anchor="center")
rrlabel = CTkLabel(master=frame, text="")
rrlabel.place(relx=0.8, rely=0.4, anchor="center")
blocklabel = CTkLabel(master=frame, text="")
blocklabel.place(relx=0.8, rely=0.4, anchor="center")

def Rickroll():
      ytimg_label.configure(image=CTkImage(Image.open("./Assets/youtube.png"), size=(180, 140)))
      ytimg_label.image = CTkImage(Image.open("./Assets/youtube.png"), size=(180, 140))

      ar1label.configure(image=CTkImage(Image.open("./Assets/arrow2.png"), size=(200, 100)))
      ar1label.image = CTkImage(Image.open("./Assets/arrow2.png"), size=(200, 100))

      grlabel.configure(image=CTkImage(Image.open("./Assets/gears.png"), size=(200, 120)))
      grlabel.image = CTkImage(Image.open("./Assets/gears.png"), size=(200, 120))

      ar2label.configure(image=CTkImage(Image.open("./Assets/arrow.png"), size=(240, 100)))
      ar2label.image = CTkImage(Image.open("./Assets/arrow.png"), size=(240, 100))

      global imgcount
      address = f"./Frames/{imgcount}.jpg"

      img = CTkImage(Image.open(address), size=(320, 200))
      rrlabel.configure(image=img)
      rrlabel.image = img
      alert.destroy()

      imgcount += 1
      if imgcount > 185:
            imgcount = 2

      app.after(60, Rickroll)

def NoRickroll():
      ytimg_label.configure(image=CTkImage(Image.open("./Assets/youtube.png"), size=(180, 140)))
      ytimg_label.image = CTkImage(Image.open("./Assets/youtube.png"), size=(180, 140))

      ar1label.configure(image=CTkImage(Image.open("./Assets/arrow2.png"), size=(200, 100)))
      ar1label.image = CTkImage(Image.open("./Assets/arrow2.png"), size=(200, 100))

      grlabel.configure(image=CTkImage(Image.open("./Assets/gears.png"), size=(200, 120)))
      grlabel.image = CTkImage(Image.open("./Assets/gears.png"), size=(200, 120))

      ar2label.configure(image=CTkImage(Image.open("./Assets/arrow.png"), size=(240, 100)))
      ar2label.image = CTkImage(Image.open("./Assets/arrow.png"), size=(240, 100))

      global imgcount
      address = f"./Frames/{imgcount}.jpg"

      base_img = Image.open(address).convert("RGBA")
      overlay_img = Image.open("./Assets/block.png").convert("RGBA").resize((400, 400))
      base_img.paste(overlay_img, (130, -20), overlay_img)

      img = CTkImage(base_img, size=(320, 200))
      rrlabel.configure(image=img)
      rrlabel.image = img
      alert.destroy()

      imgcount += 1
      if imgcount > 185:
            imgcount = 2

      app.after(24, NoRickroll)

def ResetApp():
      for lbl in [ytimg_label, ar1label, grlabel, ar2label, rrlabel, blocklabel]:
            lbl.destroy()

      urlinput.delete(0, 'end')
      submiturl.configure(state="normal")

def UpdateLists(prediction, url, datafile="links.json"):
      question = CTkLabel(master=frame, text="Has the model yielded correct prediction?", font=("Arial", 20), text_color="#8B008B")
      question.place(relx="0.5", rely="0.8", anchor="center")

      feedback_var = StringVar()
      radio1 = CTkRadioButton(master=frame, text="Yes", value="Yes", variable=feedback_var)
      radio1.place(relx=0.4, rely=0.87, anchor="center")
      radio2 = CTkRadioButton(master=frame, text="No", value="No", variable=feedback_var)
      radio2.place(relx=0.65, rely=0.87, anchor="center")

      submit = CTkButton(master=frame, text="Submit", fg_color="transparent",
                  hover_color="#4d004d", command=lambda: HandleFeedback(feedback_var.get(), prediction, url), border_width=2)
      submit.place(relx=0.5, rely=0.87, anchor="center")

      def HandleFeedback(feedback, prediction, url, datafile='links.json'):
            with open(datafile, "r") as file:
                  data = json.load(file)

            with open(datafile, "w") as file:
                  blacklist, whitelist = data["blacklist"], data["whitelist"]

                  if (prediction and feedback == "Yes") or (not prediction and feedback == "No"):
                        whitelist.remove(url) if url in whitelist else None
                        blacklist.append(url) if url not in blacklist else None
                  elif (prediction and feedback == "No") or (not prediction and feedback == "Yes"):
                        blacklist.remove(url) if url in blacklist else None
                        whitelist.append(url) if url not in whitelist else None

                  json.dump(data, file, indent=4)
            
            question.configure(text="Every single feedback counts in improving this model! Thank you!")
            submit.configure(state="disabled")
            app.after(2000, ResetApp)
            app.after(2000, destroy)

      def destroy():
            question.destroy()
            radio1.destroy()
            radio2.destroy()
            submit.destroy()

def CompareFrames(link):
      fc = 2
      ic = 0
      rrf = 0
      alert.configure(text="ANALYSING FRAMES...", text_color="#90EE90")

      while (fc < 185):
            frame = f"./Frames/{fc}.jpg"
            dependency = f"./Dependencies/{ic}.jpg"

            if not os.path.exists(frame) or not os.path.exists(dependency):
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
                              Rickroll()
                              UpdateLists(True, link)
                              break
                        else:
                              continue

            else:
                  NoRickroll()
                  UpdateLists(False, link)
                  break

      else:
            NoRickroll()
            UpdateLists(False, link)

      shutil.rmtree("./Dependencies")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    percentage = (1 - bytes_remaining / total_size) * 100
    bar = f" ↳ |{'█' * int(percentage):<50}| {percentage:.1f}%"
           
def ExtractFramesFromURL(link):
      forbidden_chars = ('/', '\\', '*', '?', ':', '<', '>', '|', '"')
      valid_title = ''
      os.mkdir('./Dependencies') if not os.path.exists('./Dependencies') else None

      try:
            print()
            yt = YouTube(link, on_progress_callback = on_progress)
            ys = yt.streams.get_highest_resolution()
            ys.download(output_path="./")
            alert.configure(text="VIDEO DOWNLOAD SUCCESSFUL...", text_color="#90EE90")

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
            alert.configure(text="Either YouTube hyperlink is invalid or video is unavailable.", text_color="#f74f4f")
            return

      finally:
            os.remove(f"./{valid_title}.mp4") if (valid_title and os.path.exists(f"./{valid_title}.mp4")) else None
            shutil.rmtree("./Dependencies") if os.path.exists("./Dependencies") else None

def VerifyLists(link, datafile="links.json"):
      with open(datafile, "r") as file:
            data = json.load(file)

            if link in data["blacklist"]:
                  submiturl.configure(state="disabled")
                  Rickroll()
                  UpdateLists(True, link)
            elif link in data["whitelist"]:
                  submiturl.configure(state="disabled")
                  NoRickroll()
                  UpdateLists(False, link)
            else:
                  threading.Thread(target=ExtractFramesFromURL, args=(link,), daemon=True).start()

def main():
      title = CTkLabel(master=frame, text="Is Rick Inside?", font=("Algerian", 60), text_color="#00FFFF")
      title.place(relx=0.5, rely=0.05, anchor="center")

      subtitle = CTkLabel(master=frame, text="By ADITYA VN KADIYALA", font=("Algerian", 20), text_color="#00FFFF")
      subtitle.place(relx=0.5, rely=0.12, anchor="center")

      enter_url = CTkLabel(master=frame, text="Enter URL:", font=("Arial", 20), text_color="#90EE90")
      enter_url.place(relx=0.05, rely=0.2, anchor="center")

      app.mainloop()

if __name__ == "__main__":
      main()