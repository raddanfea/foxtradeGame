import os
import re


class StoryObject:
    def __init__(self, game):
        self.story_states = {}
        self.current_story = None
        self.current_npc = ""
        self.story_data = self.load_story(game)

    def load_story(self, game, main="main", story="story"):
        path = str(os.path.join(game.path, 'assets', 'stories', main, story))

        if story not in self.story_states:
            self.story_states[story] = 0

        story_data = None
        with open(path, 'r') as f:
            story_data = str(f.read())
        self.current_story = story
        return re.split('\\n', story_data)

    def flip(self):
        self.story_states[self.current_story] += 1
        return True

    def do_line(self, game):

        if game.clicked == (-1000, -1000) or self.story_states[self.current_story] == 'END':
            return 0

        line = self.story_data[self.story_states[self.current_story]]

        if line.startswith('|'):
            line_list = line.split()
            command = line_list[1]
            task = line_list[2]
            target = line_list[3]

            if command == 'character':
                if task == 'show':
                    self.current_npc = target
                else:
                    self.current_npc = ''
                return self.flip()
            elif command == 'condition':
                if task == 'have_gold':
                    if game.player.gold_coin >= int(target):
                        return self.flip()
                    else:
                        game.textbox.setText(game, f'You need to earn {target} gold first.')
                if task == 'be_at':
                    if int(game.player.location) == int(target):
                        self.story_states[self.current_story] += 1
                        return True
                    else:
                        game.textbox.setText(game, f'You have nothing to do here.')

        elif line.startswith('END'):
            game.textbox.setText(game, f'You have reached the END!')
            self.story_states[self.current_story] = 'END'
        else:
            game.textbox.setText(game, line)
            self.story_states[self.current_story] += 1