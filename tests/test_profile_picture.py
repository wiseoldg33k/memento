from memento.image import crop_profile_picture
import tempfile
import os
from PIL import Image
import pytest


@pytest.fixture
def output_file():
    fd, output_file = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    yield output_file
    os.unlink(output_file)


def test_profile_picture_is_cropped(shared_datadir, output_file):
    sample_image = shared_datadir / "sample_image.jpg"

    crop_profile_picture(sample_image, output_file)

    fd_img = open(output_file, "rb")
    img = Image.open(fd_img)

    assert img.height == 200
