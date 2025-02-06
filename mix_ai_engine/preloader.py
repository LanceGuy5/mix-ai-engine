import librosa
import soundfile as sf
import pyrubberband as rubberband

from utils import loadprint

class d_Song:

  def __init__(self, file_path=None):
    """
    Initialize a d_Song object
    Maintains file and acts as a way to transform song in particular ways.

    :param file_path: Path to the file of the song to load
    """
    self.__pitch = None
    self.__tempo = None
    self.__file_path = file_path
    self.__y = None
    self.__sr = None
    self.duration = None
    
    if file_path is not None:
      self.load(file_path)
  

  '''
  Load a song into the object and store metadata about this object
  '''
  def load(self, file_path: str):
    
    if file_path is not None:
      self.__filePath = file_path

    if self.__filePath is None:
      raise Exception('No file path provided')
    

    try:
      self.__y, self.__sr = librosa.load(self.__file_path, sr=None)
    except Exception as err:
      print(f"Error occurred: {err}")
      raise Exception('Error')
  

  def get_pitch(self):
      """
      Retrieves pitch from audio data
      """
      if self.__pitch is not None:
        return self.__pitch
      if self.__y is None or self.__sr is None:
        if self.__file_path is None:
          raise Exception('Must load from a file first')
        else:
          self.load(self.__file_path)

      self.__pitch = librosa.core.piptrack(y = self.__y, sr = self.__sr)

      return self.__pitch


  def get_tempo(self):
      """
      Retrieves tempo from audio data
      """
      if self.__tempo is not None:
        return self.__tempo
      if self.__y is None or self.__sr is None:
        if self.__file_path is None:
          raise Exception('Must load from a file first')
        else:
          self.load(self.__file_path)

      self.__pitch = librosa.beat.beat_track(y = self.__y, sr = self.__sr)

      return self.__tempo
  

  def change_tempo(self, tempo_shift):
    """
    Changes the tempo of an audio file. float deviation from 1 = percent change in tempo

    :param tempo_shift: percent to change the tempo by
    """
    if self.__y is None or self.__sr is None:
        if self.__file_path is None:
          raise Exception('Must load from a file first')
        else:
          self.load(self.__file_path)
    loadprint(f'changing tempo from {self.__y} to {self.__y * tempo_shift}')
    self.__y = rubberband.time_stretch(y=self.__y, sr=self.__sr, rate=tempo_shift)
    # self.__y = librosa.effects.time_stretch(y=self.__y, rate=tempo_shift)

  
  def change_pitch(self, pitch_shift):
    """
    Changes the pitch of an audio file. 1 pitch shift = 1 semi-tone up

    :param pitch_shift: number of semitones to shift (positive = higher, negative = lower)
    """
    if self.__y is None or self.__sr is None:
        if self.__file_path is None:
          raise Exception('Must load from a file first')
        else:
          self.load(self.__file_path)
    loadprint(f'Increasing pitch {self.get_pitch()} by {pitch_shift} semi-tones')
    self.__y = rubberband.pitch_shift(y=self.__y, sr=self.__sr, n_steps=pitch_shift)
    # self.__y = librosa.effects.pitch_shift(y=self.__y, sr=self.__sr, n_steps=pitch_shift)
    

  def export_to_location(self, output_path):
    """
    Export the current song to a specific export_path

    :param output_path: Path to export the current stored y and sr as an audio file to
    """  
    if self.__y is None or self.__sr is None:
      raise Exception('No file to export')
    if output_path is None:
      raise Exception('Must provide output path')
    # TODO wrap in try catch in case of file path not existing?
    sf.write(output_path, self.__y, self.__sr, subtype='FLOAT')
