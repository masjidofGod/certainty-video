---
name: publish
description: Post a finished Certainty episode to Instagram Reels, TikTok and YouTube Shorts - the package, the post copy, the AI disclosure, each platform's settings and traps, the user's yes before every post, and the live check afterwards. Use when asked to post, publish or upload an episode, or to prepare its post copy.
---

# Publishing an episode

The episode's `publish/` folder is the source: `certainty package <ep>` fills it (the film, the covers, the
captions file, the narration as text), and `publish/README.md` holds the post copy you write with the user.

## Rules

1. **Every post waits for the user's yes**, per platform, per episode. Publishing is public and hard to undo.
2. The post copy keeps the series' rules (`${CLAUDE_PLUGIN_ROOT}/docs/rules.md`): kind words, nothing said about God that is not a
   verbatim quotation, every number one a reader can check, the sources named, how it was made stated.
3. **AI disclosure**: if the voice, music or effects were made with AI, say so in the text, and set each platform's
   AI label where it asks about realistic AI audio or video. The rules change; check them on the day.
4. The user signs in to their own accounts. Never type, store or ask for a password.

## Before posting

- `certainty check <ep>/out/film.mp4 --frames N` and `certainty safe <ep>/out/film.mp4` both pass.
- `publish/README.md` is filled in and the user approved it.

## Each platform (the settings that matter, and the traps)

| Platform | Settings | Traps |
| --- | --- | --- |
| YouTube Shorts (YouTube Studio, Create > Upload videos) | title (at most 100 characters), description, tags (comma-separated), the 9:16 cover as thumbnail; not made for kids; under Show more: paid promotion, AI use (an AI narration voice counts as realistic AI audio), category, language; Video elements > Subtitles > Upload file > With timing > the .srt; Visibility | radio buttons respond on their label text, not the circle; a vertical video under 3 minutes is a Short; confirm public with `https://www.youtube.com/oembed?url=<link>&format=json` |
| TikTok (TikTok Studio, Upload) | caption; Edit cover > Upload cover > the 3:4 cover > Save; when to post, who can see it; under Show more: AI-generated content | the cover editor's back arrow discards the cover (use Save, top right; widen the window if it is hidden); a new post may show "content under review" and "Only me" for some minutes before it settles |
| Instagram (Create > Post) | the film; crop: choose 9:16 (it may open square); Edit: Cover photo > Select from computer > the 9:16 cover; caption; Add AI label; auto-generated captions off if the captions are in the picture | the default crop cuts the frame; Share takes a minute and closes by itself: confirm on the profile |

## After posting

- Load each post and confirm it is live and public, with its cover.
- Write the three links into the episode's `decisions.md`.
- Check the profile grids later: a platform can show a video frame before the cover settles.
