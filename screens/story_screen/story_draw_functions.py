def draw_story_npc(game):
    if game.story.current_npc and game.textbox.text_state > -1 and (game.textbox.text_state % 30 != 0):
        game.screen.screen.blit(game.npc.all_npc[f'{game.story.current_npc[:game.story.current_npc.find("_")]}_speak'],
                                (
                                    game.screen.screen.get_width() * 0.5 - game.npc.all_npc[
                                        game.story.current_npc].get_width() * 0.5,
                                    0))
    elif game.story.current_npc:
        game.screen.screen.blit(game.npc.all_npc[game.story.current_npc], (
            game.screen.screen.get_width() * 0.5 - game.npc.all_npc[game.story.current_npc].get_width() * 0.5,
            0))
