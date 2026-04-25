from imap_tools import MailBox
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploads")


def fetch_email_attachments():
    """
    Fetch ONLY latest unseen email → ALL attachments
    """

    downloaded_files = []

    try:
        with MailBox("imap.gmail.com").login(EMAIL, PASSWORD, initial_folder='INBOX') as mailbox:

            # ✅ Only latest unseen email
            messages = list(mailbox.fetch('(UNSEEN)', reverse=True, limit=1))

            if not messages:
                print("📭 No new emails")
                return []

            msg = messages[0]

            print(f"📧 Email from: {msg.from_}")

            for att in msg.attachments:

                filename = att.filename or "file_from_email"
                file_path = os.path.join(DOWNLOAD_FOLDER, filename)

                # rename if exists
                if os.path.exists(file_path):
                    name, ext = os.path.splitext(filename)
                    file_path = os.path.join(DOWNLOAD_FOLDER, f"{name}_{len(downloaded_files)}{ext}")

                with open(file_path, "wb") as f:
                    f.write(att.payload)

                print(f"📥 Downloaded: {os.path.basename(file_path)}")

                downloaded_files.append({
                    "filename": os.path.basename(file_path),
                    "subject": getattr(msg, "subject", "No Subject"),
                    "from": getattr(msg, "from_", "Unknown"),
                    "date": str(getattr(msg, "date", ""))
                })

            # ✅ mark email as read AFTER processing all attachments
            mailbox.flag(msg.uid, ['\\Seen'], True)

            return downloaded_files

    except Exception as e:
        print(f"❌ Email Error: {str(e)}")
        return []