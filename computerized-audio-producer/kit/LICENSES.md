# Licences used by this kit

The kit's own code is MIT, like the rest of the repository. It installs or calls the tools below; none of them is copied into this folder. Licences were read on 2026-11-03. Check them again before you rely on them.

| Tool | Used for | Licence | Cost | Note |
| --- | --- | --- | --- | --- |
| [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) and its [weights](https://huggingface.co/ACE-Step/Ace-Step1.5) | Songs, instrumentals, beds (on Kaggle) | MIT (code and weights) | Free | The model card allows commercial use of the output but gives no guarantee against similarity to existing works. The bundled Qwen3-Embedding-0.6B is Apache-2.0. |
| [Kaggle](https://www.kaggle.com) and its [CLI](https://github.com/Kaggle/kaggle-cli) | Free GPU (weekly quota) | Kaggle terms of use; CLI is Apache-2.0 | Free | Needs an account with a verified phone number. The kit uses only a private kernel of your own. |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Optional lyrics check | MIT | Free | The Whisper model downloads on first use from Hugging Face, no login. |
| [uv](https://github.com/astral-sh/uv) (inside the kernel) | Installing ACE-Step on Kaggle | MIT OR Apache-2.0 | Free | |
| [FFmpeg](https://ffmpeg.org/legal.html) | Duration, loudness, clipping and silence checks | LGPL/GPL, depending on the build | Free | The kit calls the installed `ffmpeg`. It does not bundle it. |

## Text-to-speech models (not installed by this kit)

Cap's narration uses an open model that the owner picks. Before any commercial use, open the model page, read the licence, and write it down. Do not use a model marked non-commercial for anything that will be published or sold. Examples, checked on 2026-11-03 from the model pages (re-check, because licences change):

| Model | Licence | Commercial use |
| --- | --- | --- |
| [Phonon 31M](https://huggingface.co/gradium/phonon-31m-en) (English only, CPU) | Apache-2.0 | Yes |
| [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) | Apache-2.0 | Yes |
| [Chatterbox](https://github.com/resemble-ai/chatterbox) | MIT (outputs carry a watermark) | Yes |
| Phonon 40M models | CC BY-NC | **No** |

Models that clone a voice from a reference clip are limited to stock or synthetic voices, or the owner's own recording for the owner's own narration.
