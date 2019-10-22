from thumbnails_irekua.thumbnails import register_processor
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import librosa
import numpy as np
from PIL import Image

SIZE = (800,600)

@register_processor('audio/x-wav')
def audio_processor(item):
    hop_length = 512
    n_fft = 1024

    sig, sr = librosa.core.load(item.item_file)
    spec = np.abs(librosa.core.stft(sig))
    spec = np.log(spec+1e-9)

    scaled_spec = (spec - spec.min()) / (spec.max() - spec.min())
    img_arr = scaled_spec*255
    img_arr = img_arr.astype(np.uint8)
    img_arr = np.flip(img_arr,axis=0)
    img_arr = 255-img_arr
    
    im = Image.fromarray(img_arr)
    tmp = im.convert('RGB')
    tmp.thumbnail(SIZE,Image.ANTIALIAS)
    tmp_io = io.BytesIO()
    tmp.save(fp=tmp_io,format='JPEG')
    im_file = InMemoryUploadedFile(tmp_io, None, 'thumbnail.jpg','image/jpeg',tmp_io.getbuffer().nbytes, None)

    return im_file





