import sys
from db.knowledge_base import KnowledgeBase

try:
  name = sys.argv[1]
except:
  print("Plase enter search term.")
  exit()

kb = KnowledgeBase()
facts = kb.find(name)
kb.select_all()

print(name, facts)
