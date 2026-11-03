# Getting started

First steps for someone opening Cap for the first time. An installed bot does not have this repo on disk.

1. Check the tools. Cap looks for ffmpeg, a speech-to-text model, an open TTS model, and a free Kaggle GPU login (https://www.kaggle.com). Anything missing is listed with a free way to add it. If Kaggle is not connected, Cap works on narration and short sounds only, and says so.
2. Name the writer bot (or say you will paste scripts yourself) and the teammate that receives finished audio. Cap reaches teammates only with SendToAgent. If there is none, Cap saves files and tells you the paths.
3. Paste this as a first task: "Cap, make a 10-second test narration of this line: 'This is a short test of the audio desk.' Calm tone, two takes, with the check report. Then make an 8-second instrumental bed."
4. Cap will ask before it acts: the platform (sets the loudness target), the emotion or mood, the length, and where the files go. It writes a short diagnosis with the cost, which should be zero, and waits for your OK before it makes anything.
5. To say no, reply "no" or "stop". Cap discards the pending takes, sends nothing, and asks what to change.
