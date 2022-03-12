# Absurdle

Wordle is a word game where the player attempts to guess a 5-letter English word. Each incorrect guess receives feedback in the form of colored tiles indicating how closely the letter matches the target word. This image shows a game with 4 guesses (*arise, route, rules, rebus*) for the target word, *rebus*. Guessed letters that exactly match the target word are marked green while letters that are in the target word (but not in the right position) are marked yellow. Letters that aren't in the target word are marked gray.

![Wordle 196 example](https://upload.wikimedia.org/wikipedia/commons/e/ec/Wordle_196_example.svg)

This result is typically expressed using a **pattern** of square emojis: each square corresponds to a letter.

> ⬜🟨⬜🟨🟨<br>
> 🟩⬜🟨⬜🟨<br>
> 🟩🟨⬜🟨🟩<br>
> 🟩🟩🟩🟩🟩

**Absurdle** is a variant of Wordle coined by [qntm](https://qntm.org/absurdle):

> Wordle picks a single secret word at the beginning of the game, and then you have to guess it. Absurdle gives the impression of picking a single secret word, but instead what it actually does is consider the entire list of all possible secret words which conform to your guesses so far. Each time you guess, Absurdle prunes its internal list as little as possible, attempting to intentionally prolong the game as much as possible.

By completing this assignment, students will be able to:

- Implement a well-designed Java class to meet a given specification.
- Use sets and maps to create and manipulate nested collections of data.
- Follow prescribed conventions for code quality, documentation, and readability.

## A game of Absurdle

Suppose the Absurdle manager only knows the following 4-letter words.

- *ally, beta, cool, deal, else, flew, good, hope, ibex*

In Absurdle, instead of beginning by choosing a word, the manager narrows down its set of possible answers as the player makes guesses. If the player guesses "argh" as the first word, the Absurdle manager considers all the possible patterns corresponding to the guess.

- ⬜⬜⬜⬜ — *cool, else, flew, ibex*
- ⬜⬜⬜🟨 — *hope*
- ⬜⬜🟨⬜ — *good*
- 🟨⬜⬜⬜ — *beta, deal*
- 🟩⬜⬜⬜ — *ally*

The manager picks the pattern that contains the largest number of target words. In this case, it would pick the pattern ⬜⬜⬜⬜ corresponding to the target words *cool, else, flew, ibex*. If the player then guesses "beta", the manager chooses between the following possible patterns.

- ⬜⬜⬜⬜ — *cool*
- ⬜🟨⬜⬜ — *else, flew*
- 🟨🟨⬜⬜ — *ibex*

The manager would pick ⬜🟨⬜⬜ corresponding to the target words *else, flew*. If the player then guesses "flew", the manager chooses between the following possible patterns.

- ⬜🟩🟨⬜ — *else*
- 🟩🟩🟩🟩 — *flew*

In this case, there's a tie between the possible patterns because both patterns include only 1 target word. The manager chooses the pattern ⬜🟩🟨⬜ not because it would prolong the game, but because ⬜🟩🟨⬜ appears before 🟩🟩🟩🟩 when considering the patterns in sorted order. By coincidence rather than intention, this rule helps the manager prolong the game.

After this, there's only a single target word, *else*. The game ends when the player guesses the target word and the manager is left with no other option but to return the pattern 🟩🟩🟩🟩.

## Scaffold and check files

This repository has two subdirectories: the assignment **scaffold** and the assignment **check** files. Students only need to implement the `AbsurdleManager` class in the assignment scaffold by following the directions below. Compile and run the `AbsurdleMain` class to play a game of Absurdle using any one of the three provided dictionaries.

- `dictionary1.txt` contains the official list of 2309 5-letter words used in Wordle.
- `dictionary2.txt` contains the 9 4-letter words used in the example game above.
- `dictionary3.txt` contains 30 5-letter words for testing with a slightly larger word list.

The assignment check files include a `compare.py` shell script that programmatically plays several games using [pexpect](https://github.com/pexpect/pexpect) and compares the result against the expected output using [icdiff](https://github.com/jeffkaufman/icdiff). The script requires a completed `AbsurdleManager` class and JDK 11 or above. Compile the `AbsurdleManager` class and run the script.

```sh
javac AbsurdleManager.java && python3 compare.py
```

## Constructor

### `public AbsurdleManager(Collection<String> dictionary, int length)`

Given a dictionary of words and the target word length, initializes a new game of Absurdle. The set of words should initially contain all words from the dictionary of the given length, eliminating any duplicates. Throws an `IllegalArgumentException` if the given length is less than 1. Assume the given dictionary contains only non-empty strings composed entirely of lowercase letters.

## Methods

### `public Set<String> words()`

The client calls this method to get access to the current set of words considered by the manager.

### `public static String patternFor(String word, String guess)`

This static method is used to generate the pattern for a given target word and guess. This would typically be a private method, but it is public to enable us to test your implementation. Assume the target word has the same length as the guess, and that both strings include only lowercase letters. The algorithm for generating a pattern should abide by Wordle's rules for 🟨 yellow square tiles when a letter appears more than once.

- `patternFor("abbey", "bebop")` — 🟨🟨🟩⬜⬜. Notice how the middle letter 'b' in the guess "bebop" is green, while the first letter 'b' is yellow. Green tiles are assigned before yellow tiles.
- `patternFor("abbey", "keeps")` — ⬜🟨⬜⬜⬜. Notice how only the first letter 'e' in the guess "keeps" is yellow, while the second letter 'e' is gray. If there are multiple places for a yellow tile, choose the leftmost places.

### `public String record(String guess)`

The client calls this method to record a guess. Using the given guess, this method determines the next set of words under consideration and returns the pattern for the guess. Throws an `IllegalStateException` if the if the set of words is empty, and throws an `IllegalArgumentException` if the guess does not have the correct length. Assume the guess contains all lowercase letters.

## Implementation guidelines

Use `TreeSet` and `TreeMap` implementations for all sets and maps in this assignment. When working with strings in this assignment, use the `length` and `charAt` methods; don't call `toCharArray` as it will create an unnecessary extra `char[]` data structure.

### `patternFor(String word, String guess)`

To implement this method, keep track of the number of times each letter appears in the target word, decrement the count when assigning green tiles, and decrement the count when assigning yellow tiles. Tiles not assigned green or yellow are gray. For example, to compute `patternFor("abbey", "bebop")`:

1. ❔❔🟩❔❔ — assign green tiles first.
2. 🟨🟨🟩❔❔ — assign yellow tiles next.
3. 🟨🟨🟩⬜⬜ — assign gray tiles last.

Use the following data structures in this method.

- `Map<Character, Integer> counts` to keep track of the count for each letter in the target word.
- `String[] pattern = new String[word.length()]` to store the assigned green, yellow, and gray tiles. Each index in pattern stores one of the three types of tiles: `"🟩"`, `"🟨"`, or `"⬜"`. Construct the final string result from this pattern by appending all the tiles.

> ⚠️ We can't use a `char[]` pattern because of limitations in the `char` type for tiles. **Your tiles must be stored as strings!**

### `record(String guess)`

For each call to `record`, construct a `Map` to associate patterns with target word sets and use it to find all pick the pattern associated with the largest number of target words. When there are multiple patterns that have the same largest number of target words, pick the pattern that appears first in the sorted order, i.e. the pattern that appears earliest when iterating over the `TreeMap`. The associated target words becomes the dictionary for the next call to `record`.

> ⚠️ It's necessary to construct a new `Map` on each call to record because the patterns depend on the given guess!

## Development strategy

Implement the constructor and the `words` method first. Then, implement and test the `patternFor` static method. If your `patternFor` method is not working, your `record` method also will not work!

`AbsurdleMain` has two constants that you will want to change:

- `DICTIONARY_FILE` represents the name of the file containing the list of initial words. By default, it reads from `dictionary1.txt`, which contains the official list of 2309 5-letter words used in Wordle. When testing, it may be easier to use the `dictionary2.txt` file that only contains 9 4-letter words.
- `SHOW_COUNT` is `false` by default; set it to `true` to see the number of words under consideration.

## Self-check questions

### Question 1

In the example with 4-letter words, we described what happens when the manager has the target words *cool, else, flew, ibex*.

When the player guesses "beta", the manager chooses between the following possible patterns.

- ⬜⬜⬜⬜ — *cool*
- ⬜🟨⬜⬜ — *else, flew*
- 🟨🟨⬜⬜ — *ibex*

Why did the manager choose the pattern ⬜🟨⬜⬜?

- [ ] The pattern contained the largest number of ⬜ gray square tiles.
- [ ] The pattern contained the largest number of 🟨 yellow square tiles.
- [ ] The pattern corresponds to the largest number of target words.
- [ ] The pattern corresponds to the smallest number of target words.
- [ ] The pattern appears earlier in sorted order.
- [ ] The pattern appears later in sorted order.

### Question 2

After the next guess, we described what happens when the manager has the target words *else, flew*.

When the player guesses "flew", the manager chooses between the following possible patterns.

- ⬜🟩🟨⬜ — *else*
- 🟩🟩🟩🟩 — *flew*

Why does the manager choose the pattern ⬜🟩🟨⬜ instead of 🟩🟩🟩🟩?

- [ ] The pattern contained the largest number of ⬜ gray square tiles.
- [ ] The pattern contained the largest number of 🟨 yellow square tiles.
- [ ] The pattern corresponds to the largest number of target words.
- [ ] The pattern corresponds to the smallest number of target words.
- [ ] The pattern appears earlier in sorted order.
- [ ] The pattern appears later in sorted order.

### Question 3

Suppose we started a new game of Absurdle with the possible 4-letter target words *dogs, cats, bird*.

If the player guesses "dirt", what patterns will be generated in the `record` method?

- [ ] ⬜⬜⬜⬜
- [ ] ⬜⬜⬜🟨
- [ ] ⬜⬜🟨⬜
- [ ] ⬜🟩🟩🟨
- [ ] 🟨🟩🟩⬜
- [ ] 🟩⬜⬜⬜
