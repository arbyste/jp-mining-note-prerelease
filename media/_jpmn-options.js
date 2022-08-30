// JPMN is short for JP Mining Note
var JPMNOpts = (function (my) {

  my.settings = {
      // RESERVED KEYS (by anki):
      // - e (edit)
      // - r (replay)
      // - t (stats)
      // - y (sync)
      // - i (card info)
      // - o (options)
      // - a (add)
      // - s (idk exactly what this does tbh)
      // - d (deck)
      // - f (filtered deck options)
      // - v (play recorded voice)
      // - b (browse)
      // - m (menu)
      // - 1, 2, 3, 4 (again, hard, good, easy)
      // - 5 (pause audio)
      // - 6 (audio -5s)
      // - 7 (audio +5s)
      // - space (good)
      // - enter (good)
      //
      // RESERVED KEYS (by AJT Flexible grading):
      // - u (undo)
      // - h, j, k, l: hard / again / good / easy
      //
      // FREE KEYS:
      // - (left)  q w g z x c
      // - (right) p n 8 9 0 , . ; ' [ ]
      "keybinds": {
        // Keybind to toggle between showing the sentence and word on click and hover cards.
        // Equivalent to either clicking on the sentence/word on a click card,
        // or hovering over the word on a hover card.
        "toggle-hybrid-sentence": ["n"],

        // Keybind to toggle between showing the tested word in a raw sentence card.
        // Equivalent to clicking on the "show" button.
        // This is the same as the above because both should never happen at the same time.
        "toggle-highlight-word": ["n"],

        // Keybind to toggle a vocab card's full sentence display (front side).
        // Techinically can be Shift / n as it doesn't interfere with the other two above.
        "toggle-front-full-sentence-display": ["'"],

        "play-sentence-audio": ["p"],

        "play-word-audio": ["w"],

        // Equivalent to toggling the hint show/hide
        "toggle-hint-display": ["."],

        "toggle-secondary-definitions-display": ["8"],

        "toggle-additional-notes-display": ["9"],

        "toggle-extra-definitions-display": ["0"],

        "toggle-extra-info-display": ["["]
      },

      "sentence": {
        // Automatic processing to sentences
        "enabled": true,

        // Removes all line breaks on the regular sentence (if AltDisplay is not filled)
        // TODO mobile true, desktop false
        "remove-line-breaks": false,

        // Removes all line breaks on the AltDisplay sentence
        // TODO mobile true, desktop false
        "remove-line-breaks-on-altdisplay": false,

        // colors the quotes instead of showing a pitch accent indicator
        // if this is enabled
        // TODO mobile true, desktop false
        "pa-indicator-color-quotes": false,

        // automatically colors the quote with the sentence pa indicator color,
        // on PA sentence cards
        "pa-sent-pa-indicator-color-quotes": false,

        // automatically adds quotes to the sentence (if not alt display)
        "auto-quote-sentence": true,

        // automatically adds quotes to the sentence (if alt display)
        "auto-quote-alt-display-sentence": true,

        // the quote pair to automatically add to the sentence
        "auto-quote-open": "「",
        "auto-quote-close": "」",

        // the quote pair to automatically add to the sentence if it's a PA sentence card
        "pa-sent-auto-quote-open": "『",
        "pa-sent-auto-quote-close": "』",

        // quotes to search for on existing sentences,
        // to not double-quote a sentence that already has quotes on it
        "quote-match-strings": [
          ["「", "」"],
          ["『", "』"]
        ]
      },

      // Hover over a kanji in the word reading to see if it has been used
      // in previous cards or not.
      "kanji-hover": {
        "enabled": true,

        // 0: loads every time, slower to reveal the back side of the card
        // 1: loads only upon hover, has a small delay upon first hovering over a word
        "mode": 1,

        // all queries will have the following at the beginning:
        // (-"Key:{{ T('Key') }}" Word:*${character}* "card:${cardTypeName}")

        // not new, or new and green
        // not flagged as red and suspended
        "non-new-query": "(-is:new OR (is:new flag:3)) -(is:suspended flag:1)",

        // new
        // not suspended, and neither flagged as red or green
        "new-query": "is:new -(is:suspended (flag:1 OR flag:3))",

        // maximum number of words per category
        "max-non-new-oldest": 2,
        "max-non-new-latest": 2,
        "max-new-latest": 2
      },


      // Overrides the play keybind button to show the sentence if the
      // card is a hybrid sentence AND the sentence is not currently being shown.
      // Only affects the front side.
      "hybrid-sentence-open-on-play-sentence": true,

      // By default, the indicator for collapsable fields are completely removed.
      // Making this true keeps the indicator, but greys out the text to show that
      // it cannot be opened.
      "greyed-out-collapsable-fields-when-empty": false,

      // Opens the "extra info" field if the card is new.
      // Useful for checking pitch accent, etc.
      "open-extra-info-when-new": false,

      // (Developer option) Used to show debug messages when debugging the card.
      // Use the `_debug()` function in javascript to write debug messages.
      "debug": false
    }

  return my;
}(JPMNOpts || {}));
