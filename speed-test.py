import tkinter as tk
from tkinter import Label, StringVar
import speedtest
from PIL import Image, ImageTk
import threading

# Class to represent the Internet Speed Test Application
class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("450x540")
        self.root.config(bg="#2f2f2f")
        self.root.resizable(False, False)
        self.root.iconbitmap('./images/speed.ico')

        # Load gauge image
        self.load_gauge_image()

        # StringVars to hold the text values for ping, download, and upload speed
        self.ping_var = StringVar(value="Ping: -- ms")
        self.download_var = StringVar(value="Download: -- \nMbps")
        self.download_var_main = StringVar(value="Download: -- Mbps")
        self.upload_var = StringVar(value="Upload: -- \nMbps")

        # Create labels for displaying ping, download, and upload speed
        self.create_speed_labels()

        # Create Start button
        # Creating a photoimage object to use image
        self.start_photo = ImageTk.PhotoImage(file = "./images/start.png") 
        # Resizing image to fit on button 
        self.start_button = tk.Button(root, image = self.start_photo, command=self.start_speed_test, bg="#2f2f2f", bd=0, activebackground="#2f2f2f")
        self.start_button.place(x=110, y=460)

    # Method to load and place the gauge image
    def load_gauge_image(self):
        # Load the gauge image using PIL
        image = Image.open("./images/gauges.png")
        self.gauge_img = ImageTk.PhotoImage(image)

        # Place the gauge image
        self.gauge_label_ping = Label(self.root, image=self.gauge_img, bg="#2f2f2f")
        self.gauge_label_ping.place(x=1, y=5)

        # Load the main gauge image using PIL
        main_image = Image.open("./images/gauge-main.png")
        main_image = main_image.resize((400, 300), Image.ANTIALIAS)
        self.main_img = ImageTk.PhotoImage(main_image)
        self.main_gauge_label = Label(self.root, image=self.main_img, bg="#2f2f2f")
        self.main_gauge_label.place(x=10, y=150)

    # Method to create labels for the speed values (Ping, Download, Upload)
    def create_speed_labels(self):
        self.ping_label = Label(self.root, textvariable=self.ping_var, font=("Arial", 10), fg="white", bg="#2f2f2f")
        self.ping_label.place(x=30, y=75)

        self.download_label = Label(self.root, textvariable=self.download_var, font=("Arial", 10), fg="white", bg="#2f2f2f")
        self.download_label.place(x=179, y=75)

        self.upload_label = Label(self.root, textvariable=self.upload_var, font=("Arial", 10), fg="white", bg="#2f2f2f")
        self.upload_label.place(x=335, y=75)

        self.download_label = Label(self.root, textvariable=self.download_var_main, font=("Arial", 14), fg="white", bg="#2f2f2f")
        self.download_label.place(x=120, y=285)



    # Method to start the speed test in a separate thread (to avoid blocking the GUI)
    def start_speed_test(self):
        threading.Thread(target=self.run_speed_test).start()

    # Method that performs the actual speed test and updates the UI
    def run_speed_test(self):
        # Instantiate speedtest object
        st = speedtest.Speedtest(secure=True)

        # Measure Ping
        self.ping_var.set("Ping: Testing")
        ping_result = st.results.ping
        self.ping_var.set(f"Ping: {ping_result:.2f} ms")

        # Measure Download Speed
        self.download_var.set("Download: Testing")
        self.download_var_main.set("Download: Testing...")
        download_result = st.download() / 1_000_000  # Convert to Mbps
        self.download_var.set(f"Download: {download_result:.2f} \nMbps")
        self.download_var_main.set(f"Download: {download_result:.2f} Mbps")

        # Measure Upload Speed
        self.upload_var.set("Upload: Testing")
        upload_result = st.upload() / 1_000_000  # Convert to Mbps
        self.upload_var.set(f"Upload: {upload_result:.2f} \nMbps")

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()