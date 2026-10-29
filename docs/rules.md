# The rules

The kit is made for films about the Quran's numbers that a viewer can check for themselves. These rules keep them
checkable and kind. The skills and the commands enforce what they can; the rest is yours.

## The evidence

1. **Every number is computed, never typed.** A number on screen or in the narration is a claim in `claims.toml`,
   and `certainty verify` says it matches the data. The timeline reads it through `verify.measured()`.
2. **Every quotation is verbatim**, from the data, with its address. Arabic on screen is shaped from the data by
   `certainty glyphs`, never typed or drawn by hand.
3. **Nothing is said about God that is not a verbatim quotation.** Paraphrase the pattern, never God.
4. **Claims that need a counting rule say the rule.** If a count holds only when something is counted a certain
   way, say so on screen, or leave the claim out.
5. **Sources are the Quran and named, current sources.** Name them in the script's Sources table and in the post.

## The tone

6. **Kind words.** The viewer's doubt is welcome; answer it by counting together. No mockery, no challenge.
7. **An honest limit.** One pattern alone could be chance; say so when it fits.

## Money and publishing

8. **Nothing that costs money runs without a yes.** `voice` and `music` are dry runs until `--yes`.
9. **Nothing is posted without a yes**, for each post on each platform.
10. **Say how it was made.** If a voice, music or effect was made with AI, say so in the post, and use each
    platform's AI label where it asks for one.

## The picture

11. **Inside the safe area.** Everything to be read stays inside x 80 to 1000 and y 280 to 1440, and inside x 180
    to 900 below y 900 (the platforms' buttons and captions). `certainty safe` checks the film.
12. **Stills before motion.** Review full-size stills, then a 480p draft, then render the film once.
