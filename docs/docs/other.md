

design decisions with main template:

- everything should be available to the user even for words with very long definitions
    - the definitions are below everything specifically due to that
    - potential issue: people who speed through cards
    - potential solution: use theme
- front side has no guarantee to be consistent
    - thus, word is repeated again below the line
    - also see: cardtypes.md
- word and pitch accent are on separate lines
    - because both can expand very far to the left/right
- minimize vertical space taken from word info / image
    - if certain elements are removed, can result in an uneven shape
    - however, this is preferable over an even shape because it minimizes vertical space
    - TODO option to have a consistent shape?


design decisions with mobile template:

- make definition show up ASAP, i.e. by the first quarter of the screen
    - this means elements that were previously above the definition on the PC version, like the audio buttons, image, and sentence, is now below the definition

    - unfortunately, putting the sentence above the definition can easily take up a lot of room
        - the limited space for mobile users makes placing the definition above the sentence
            actually more important, otherwise the sentence can easily push down the bulk of the definition
            (and thus you must scroll to see the definition)
        - comes at the cost of potentially not being able to see the sentence without scrolling
    - the image is small by design
        - otherwise, will take up too much room or will require scrolling to see
        - goal is to always be able to immediately see the image on card flip

- button friendly
    - replace collapsible sections with buttons for easier mobile navigation

- furigana removed because of vertical space








This page showcases many examples on how you can customize the user interface to your liking.
As there are many examples that you likely won't use,
I recommend quickly skimming through this page to see if there is anything you would like
your note to do.

!!! note
    * If you want to change something for a card-per-card basis, see the [Field Reference](fieldref.md) page.
    * These customizations make heavy use of {{ RTOs }} and {{ C_CSS }}.

---


# Remove the "(N/A)" on cards with no pitch accents
{{ feature_version("0.11.0.0") }}

If the word has no pitch accent, the pitch accent is usually displayed as `(N/A)`.
This indicator can be removed with the following {{ CSS }}:

??? example "Instructions *(click here)*"

    1. Under `extra/style.scss`, add the following code:

        ```css
        .dh-left__word-pitch-text:empty:before {
          content: ""
        }
        ```

---





# Removing the furigana on the word reading

The following {{ CSS }} removes the furigana on the word reading, while keeping
the furigana on the kanjis within hover.

TODO image

??? example "Instructions *(click here)*"

    1. Under `extra/style.scss`, add the following code:

        ```css
        .dh-left__reading > ruby > rt {
          display: none;
        }
        ```

---




# Changing colors
Most color changes can be done by simply editing a CSS variable.
These variables are shown at the very top of the main CSS sheet.
For example, the following changes the main accent color of the card:

??? example "Instructions *(click here)*"

    1. Under `extra/style.scss`, add the following code:

        ```css
        :root {
          --accent: #ff1fd1; /* hot pink */
        }

        .night_mode {
          --accent: #ff7777; /* light red */
        }
        ```

    !!! note
        To change any variable color for dark mode, you cannot use `:root`, even if you are only setting
        the color for night mode. You must use `.night_mode`.

        For example, doing the following will NOT change the accent for night mode:
        ```css
        :root {
          /* only changes light mode accent, and will NOT change dark mode accent! */
          --accent: #ff7777;
        }
        ```

        You must do this instead:
        ```css
        /* changes the color for both light and dark mode */
        :root {
          --accent: #ff7777;
        }
        .night_mode {
          --accent: #ff7777;
        }
        ```

---


# Removing the word / sentence at the top of the back side

{{ feature_version("0.11.1.0") }}

For users who are only using one card type
(e.g. only vocab cards with no sentence cards, TSCs, or anything else),
it might be better to remove the tested content and the line below it.

TODO image

The tested content is shown at the back by default to allow the user to differentiate
between card types on both sides of the card.
However, this take up extra vertical space which is unnecessary if you are only using one card type.

??? example "Instructions *(click here)*"

    Use the following {{ CSS }}:

    1. Under `extra/style.scss`, add the following code:

        ```css
        .card-main--back .expression-wrapper {
          display: none;
        }
        ```

---




# Conclusion
Outside of the user interface, the note has plenty of fields you can use
to further modify the card. Head over to the [Field Reference](fieldref.md) page to see just that.