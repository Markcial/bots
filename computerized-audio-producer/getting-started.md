# Getting started

First steps for someone opening Cap for the first time. An installed bot does not have this repo on disk.

1. Cap needs a computer with a shell and internet access (ffmpeg, Python, the Kaggle command line). Say `Set up your workspace.` Cap tells you what it will install, asks for your yes, fetches its kit from `github.com/Markcial/bots/computerized-audio-producer/kit`, runs `setup.sh` and `doctor.sh`, and shows you the result. For songs you also need a free Kaggle account with a verified phone and an API token from https://www.kaggle.com/settings/api. You create those yourself and save the token where the Kaggle command line reads it (`kaggle auth login`, or `~/.kaggle/access_token`, or `~/.kaggle/kaggle.json` with `chmod 600`). Cap never sees your password and never asks for the token in chat. Without Kaggle, Cap does narration and short sounds only and says so.
2. Name the writer bot (or say you will paste scripts yourself) and the teammate that receives finished audio. Cap reaches teammates only with SendToAgent. If there is none, Cap saves files and tells you the paths.
3. Paste this as a first task: "Cap, make a 10-second test narration of this line: 'This is a short test of the audio desk.' Calm tone, two takes, with the check report. Then make an 8-second instrumental bed."
4. Cap will ask before it acts: the platform (YouTube and social are about -14 LUFS, podcasts about -16), the emotion or mood, the length, and where the files go. It writes a short diagnosis with the cost, which should be zero, and waits for your OK before it makes anything.
5. To say no, reply "no" or "stop". Cap discards the pending takes, sends nothing, and asks what to change.
