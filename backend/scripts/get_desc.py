import json
import llm


with open('players.json') as f:
  players = json.loads(f.read())

model = llm.get_model("gemini-2.5-pro")
updated_players = []
resp = model.prompt(f"Create a short description for the baseball player with the stats given by this json snippet:\n{players[0]}")
print(resp.text())
print(resp)
# for player in players[0:2]:
#   resp = model.prompt(f"Create a short description for the baseball player with the stats given by this json snippet:\n{player}")
#   print(resp.text())


