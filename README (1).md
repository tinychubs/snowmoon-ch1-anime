# Snowmoon, Chapter 1: Anime Adaptation (Process Repo)

By TinychubsX (https://x.com/TinychubsX)

A short anime film of Chapter 1 of [Snowmoon](https://vitalik.eth.limo/snowmoon), planned as twenty 10-second scenes with Japanese narration and dialogue and English subtitles.

**Watch (HD):** link coming soon

Made for the "Bring Snowmoon to Life" bounty. Snowmoon is published under GPL v3, and its author intends for people to make films and anime adaptations as long as the production materials behind them are open-sourced. This repo is that open release.

## Files

| File | Contents |
|---|---|
| `SCRIPT.md` | Narration (10 lines) and all character dialogue in Japanese and English |
| `STORYBOARD.md` | Beat-by-beat storyboard for all 20 scenes |
| `PROMPTS.md` | Character and prop reference sheet prompts, city multiview prompts, and one video prompt per scene |
| `scenes.json` | The whole 20-scene plan as structured data (timecode, beats, narration, dialogue, audio notes, video prompt) |
| `production-brief.pdf` | The full production brief (character sheets, city multiview, 20 scene cards, dialogue coverage checklist) |
| `build_brief_pdf.py` | The script that generates the production brief PDF |

## Process

1. **Script.** Chapter 1 was split into visual beats (about 85), then condensed to 25 scenes and finally to 20 by merging beats that could share one 10-second clip. Narration and dialogue were written in Japanese with English translation, kept under about 55 to 70 Japanese characters per scene so the speech fits inside 10 seconds. (Claude)
2. **Prompts and storyboard.** Generation prompts and the storyboard were written and refined. (ChatGPT)
3. **Reference sheets.** One reference sheet per main character, the toy drone and key props, plus a city multiview sheet, reused in every scene to keep faces, outfits and environments consistent.
4. **Video generation.** Each scene was generated from its prompt with the matching reference images, mainly with Seedance, plus Grok Imagine and Google Flow for other shots. Clips were regenerated and swapped until each matched its storyboard beats.
5. **Voice.** Japanese narration with Fish Audio. Character lines recorded from `SCRIPT.md`. Ambience, music and effects added following the audio notes in each scene.
6. **Edit and finish.** Clips assembled in order with hard cuts and deliberate camera motion. UI and text overlays (vote screen, watch checks, rubric, bus posters, messages) composited by hand so they stay crisp and readable. English subtitles added and the final audio mixed by hand.

Consistency rules: the same style lock is added to every image and video prompt, and Gladias wears the purple privacy robe with the hood down early on, hood up at the concert, and hood down again afterwards.

## Tools and models

| Stage | Tool | Used for |
|---|---|---|
| Script | Claude (Anthropic) | Narration and dialogue in Japanese and English, the scene breakdown, and the production brief |
| Prompts and storyboard | ChatGPT (OpenAI) | Writing and refining the generation prompts and the storyboard |
| Video | Seedance (main tool) | Most of the 10-second scene clips |
| Video | Grok Imagine | Additional clips and shots |
| Video | Google Flow | Additional clips and shots |
| Narration voice | Fish Audio | Japanese narrator track |
| Character dialogue voices | **TO CONFIRM** | Japanese voices for the characters |
| Character sheets and image references | **TO CONFIRM** | Reference images generated from the prompts in `PROMPTS.md` |
| Editing, compositing, audio mix | **TO CONFIRM** | Hard cuts, camera motion, overlays, subtitles, final mix |

Custom tooling: `build_brief_pdf.py` (Python and ReportLab) builds the brief PDF, and `scenes.json` holds the scene data so other tooling can use it.

## Changes from the brief

The original 20-scene plan included child and teenage characters from the story. The moderators of the bounty platform removed the first upload because minors appear in it, so the resubmitted film has the minors removed. The production brief PDF is the original plan, kept as a record of the process.

Scenes in the original plan that featured minors: 4, 15, 16, 17, 18, 19 and 20. Narration lines N8 (Scene 16) and N9 (Scene 18) also refer to the children.

| Scene | Minors in the original plan | What changed in the submitted cut |
|---|---|---|
| 04 | The drone boy, his two younger siblings, and a child with the grandmother | **TO CONFIRM** |
| 15 | A teenager on the bus | **TO CONFIRM** |
| 16 | Zven (younger son) and Febric (teenage boy) | **TO CONFIRM** |
| 17 | Zven and Febric | **TO CONFIRM** |
| 18 | Lily (daughter) | **TO CONFIRM** |
| 19 | Zven, Febric and Lily | **TO CONFIRM** |
| 20 | The family in the background | **TO CONFIRM** |

## Notes

- **Adapted wording.** The narration and dialogue are adapted in original wording to fit 10-second pacing. The story text itself is not reproduced in this repo.
- **Concert lyric.** The Dreadknot lyric in Scene 8 is a new placeholder line written for the film.

## Build the brief PDF

```bash
pip install reportlab
# JP_FONT must be a TrueType font with Japanese glyphs (not a CFF-based .otf)
JP_FONT=/path/to/japanese-font.ttc OUT=brief.pdf python build_brief_pdf.py
```

## License

This repository is released under the GNU General Public License v3.0 (GPL-3.0), matching the license of Snowmoon. See `LICENSE`. Third-party tools and models (Seedance, Grok Imagine, Google Flow, Fish Audio, ChatGPT, Claude) are not redistributed here and remain under their own terms.
