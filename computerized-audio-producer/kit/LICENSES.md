# Licences used by this kit

The kit's own code is MIT, like the rest of the repository. It installs or calls the tools below; none of them is copied into this folder. Licences were read on 2026-11-03. Check them again before you rely on them.

| Tool | Used for | Licence | Cost | Note |
| --- | --- | --- | --- | --- |
| [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) and its [weights](https://huggingface.co/ACE-Step/Ace-Step1.5) | Songs, instrumentals, beds (on Kaggle) | MIT (code and weights) | Free | The model card allows commercial use of the output but gives no guarantee against similarity to existing works. The bundled Qwen3-Embedding-0.6B is Apache-2.0. |
| [Kaggle](https://www.kaggle.com) and its [CLI](https://github.com/Kaggle/kaggle-cli) | Free GPU (weekly quota) | Kaggle terms of use; CLI is Apache-2.0 | Free | Needs an account with a verified phone number. The kit uses only a private kernel of your own. |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Optional lyrics and narration word check | MIT | Free | The Whisper model downloads on first use from Hugging Face, no login. |
| [uv](https://github.com/astral-sh/uv) (inside the kernel) | Installing ACE-Step on Kaggle | MIT OR Apache-2.0 | Free | |
| [FFmpeg](https://ffmpeg.org/legal.html) | Duration, loudness, clipping and silence checks; synthesised sound effects | LGPL/GPL, depending on the build | Free | The kit calls the installed `ffmpeg`. It does not bundle it. Effects made by `make_sfx.py` come from maths and noise: no assets, nothing to credit. |
| [ptts](https://github.com/gradium-ai/xn-ptts) and [Phonon 31M](https://huggingface.co/gradium/phonon-31m-en) with its [voices](https://huggingface.co/gradium/phonon-voices) | Narration on the CPU (`narrate.py`) | Apache-2.0 (runtime, model and voices) | Free | English only. The model (about 60 MB) downloads on first use from Hugging Face, no login. AI-generated speech: say so when you publish it. |

## Text-to-speech models (only Phonon 31M is installed by this kit)

`narrate.py` uses Phonon 31M by default and refuses the Phonon 40M models unless `--non-commercial` is passed. Any other model or engine needs `--licence` with what you read on its model page, written into the output manifest. Before any commercial use, open the model page, read the licence, and write it down. Do not use a model marked non-commercial for anything that will be published or sold. Examples, checked on 2026-11-03 from the model pages (re-check, because licences change):

| Model | Licence | Commercial use |
| --- | --- | --- |
| [Phonon 31M](https://huggingface.co/gradium/phonon-31m-en) (English only, CPU) | Apache-2.0 | Yes |
| [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) | Apache-2.0 | Yes |
| [Chatterbox](https://github.com/resemble-ai/chatterbox) | MIT (outputs carry a watermark) | Yes |
| Phonon 40M models ([English](https://huggingface.co/gradium/phonon-40m-en), multilingual, French, German, Spanish, Portuguese) | CC BY-NC 4.0 | **No**. Refused by `narrate.py` without `--non-commercial`. |

Models that clone a voice from a reference clip are limited to stock or synthetic voices, or the owner's own recording for the owner's own narration. `narrate.py` accepts only stock catalog voice names and has no reference-audio option.

## Sounds you provide

`make_sfx.py --import-dir` accepts CC0 or public-domain files only, with the licence you read on the page each file came from, recorded in `sfx-manifest.json`. CC BY needs credit and CC BY-NC or "personal use" is not enough to publish: do not import those.
