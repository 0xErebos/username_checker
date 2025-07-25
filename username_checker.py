import customtkinter as ctk
import threading
import requests
from urllib.parse import urlparse

platform_links = [
    "https://www.instagram.com/", "https://www.tiktok.com/@", "https://x.com/",
    "https://www.facebook.com/", "https://www.youtube.com/@", "https://www.snapchat.com/@",
    "https://www.reddit.com/user/", "https://www.linkedin.com/in/", "https://www.twitch.tv/",
    "https://www.pinterest.com/", "https://www.quora.com/profile/", "https://www.flickr.com/people/",
      "https://www.behance.net/", "https://www.deviantart.com/", "https://www.paypal.com/paypalme/",
    "https://www.soundcloud.com/", "https://www.spotify.com/user/", "https://www.medium.com/@",
    "https://www.vimeo.com/user/", "https://www.github.com/", "https://www.gitlab.com/",
    "https://www.bitbucket.org/", "https://www.codepen.io/", "https://www.stackoverflow.com/users/",
    "https://www.slack.com/team/", "https://www.discord.com/users/", "https://www.tumblr.com/",
    "https://www.wattpad.com/user/", "https://www.goodreads.com/users/",
    "https://www.reverbnation.com/", "https://www.bandcamp.com/", "https://www.mixcloud.com/",
    "https://www.last.fm/user/", "https://www.500px.com/", "https://www.flickr.com/photos/",
    "https://www.behance.net/gallery/", "https://www.patreon.com/",
    "https://www.kickstarter.com/profile/", "https://www.indiegogo.com/profile/",
    "https://news.ycombinator.com/user?id=", "https://dribbble.com/",
]

show_not_found = True

def check_username(username, callback):
    for link in platform_links:
        parsed_url = urlparse(link)
        if parsed_url.path.endswith('/'):
            full_link = f"{link}{username}"
        else:
            full_link = f"{link}{username}/"
        try:
            response = requests.get(full_link, timeout=5)
            if response.status_code == 200:
                callback(f"✅ found on {full_link}")
            else:
                if show_not_found != False:
                    callback(f"❌ found on {full_link}")
        except requests.RequestException as e:
            callback(f"❗Error checking {full_link}: {e}")

class UsernameCheckerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Username Checker")
        self.geometry("500x500")

        self.input_label = ctk.CTkLabel(self, text="Enter username:")
        self.input_label.pack(pady=(20, 5))

        self.username_entry = ctk.CTkEntry(self, width=300)
        self.username_entry.pack(pady=5)

        self.show_not_found_var = ctk.BooleanVar(value=True)
        self.check_show_not_found = ctk.CTkCheckBox(
            self,
            text="Show 'not found' results",
            variable=self.show_not_found_var,
            onvalue=True,
            offvalue=False
        )
        self.check_show_not_found.pack(pady=5)

        self.check_button = ctk.CTkButton(self, text="Check Username", command=self.start_check)
        self.check_button.pack(pady=10)

        self.result_box = ctk.CTkTextbox(self, width=650, height=350, wrap="word")
        self.result_box.pack(pady=10, padx=10, fill="both", expand=True)
        self.result_box.configure(state="disabled")

    def start_check(self):
        global show_not_found
        show_not_found = self.show_not_found_var.get()
        username = self.username_entry.get().strip()
        if not username:
            self.show_result("Please enter a username.")
            return
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", f"Checking username: {username}\n\n")
        self.result_box.configure(state="disabled")
        threading.Thread(target=self.run_check, args=(username,), daemon=True).start()

    def show_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.insert("end", text + "\n")
        self.result_box.see("end")
        self.result_box.configure(state="disabled")

    def run_check(self, username):
        def callback(msg):
            self.after(0, self.show_result, msg)
        check_username(username, callback)

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = UsernameCheckerApp()
    app.mainloop()