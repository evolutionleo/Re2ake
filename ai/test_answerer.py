from dotenv import load_dotenv
from ai import Answerer

load_dotenv()

e = Answerer()
e.answer("Hello, where can i find some lemons", {"Hello, where can i find some oranges": "You can find oranges in the fruit section of the supermarket."})
