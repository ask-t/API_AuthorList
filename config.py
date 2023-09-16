from dotenv import load_dotenv
load_dotenv()

# 環境変数を参照
import os
DATABASE=os.getenv("DATABASE")
HOST=os.getenv("HOST")
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
PORT=os.getenv("PORT")


