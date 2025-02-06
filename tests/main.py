from mix_ai_engine import d_Song

if __name__ == '__main__':
  song = d_Song('./songs/sparks.mp3')
  song.change_pitch(2)
  song.export_to_location('./songs/modified_sparks.mp3')