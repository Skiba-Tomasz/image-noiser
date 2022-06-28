import tensorflow_datasets as tfds
from pathlib import Path

class MyDataset(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for my_dataset dataset."""

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  def _info(self) -> tfds.core.DatasetInfo:
    """Dataset metadata (homepage, citation,...)."""
    return tfds.core.DatasetInfo(
        builder=self,
        features=tfds.features.FeaturesDict({
            'image': tfds.features.Image(shape=(256, 256, 3)),
            'label': tfds.features.ClassLabel(
                names=['no', 'yes'],
                doc='Whether this is a picture of a cat'),
        }),
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Download the data and define splits."""
    extracted_path = 'C:/Users/skibi/Documents/Projects/Studia/Magisterka/image-noiser/datasets/my_dataset/set/'#dl_manager.download_and_extract('http://data.org/data.zip')
    # dl_manager returns pathlib-like objects with `path.read_text()`,
    # `path.iterdir()`,...
    return {
        'train': self._generate_examples(path=Path(extracted_path + 'train')),
        'test': self._generate_examples(path=Path(extracted_path + 'test')),
    }

  def _generate_examples(self, path):
    """Generator of examples for each split."""
    for img_path in path.glob('*.jpg'):
      # Yields (key, example)
      yield img_path.name, {
          'image': img_path,
          'label': 'yes' if img_path.name.startswith('yes_') else 'no',
      }