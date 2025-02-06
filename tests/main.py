from mix_ai_engine import d_Song

if __name__ == '__main__':
  song = d_Song('./songs/get_lucky.wav')
  song.change_pitch(1)
  song.change_tempo(1.2)
  song.export_to_location('./songs/mod_use_somebody.wav')