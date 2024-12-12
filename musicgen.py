from transformers import AutoProcessor, MusicgenForConditionalGeneration
from transformers import pipeline
import scipy

def generate_a_new_song(description, name_of_the_output_file, max_new_tokens_hyperparameter=256):
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

    inputs = processor(
        text=[description],
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens_hyperparameter)
    import scipy

    sampling_rate = model.config.audio_encoder.sampling_rate
    scipy.io.wavfile.write(name_of_the_output_file, rate=sampling_rate, data=audio_values[0, 0].numpy())
