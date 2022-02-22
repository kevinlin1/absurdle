// Class AbsurdleMain is the driver program for the Absurdle program. It reads
// a dictionary of words to be used during the game and then plays a game with
// the user. You can change the setting for SHOW_COUNT to see how many options
// are still left on each turn.

import java.util.*;
import java.io.*;

public class AbsurdleMainDict2  {
    public static final String DICTIONARY_FILE = "dictionary2.txt";
    public static final int LENGTH = 4;
    public static final boolean SHOW_COUNT = true;

    public static void main(String[] args) throws FileNotFoundException {
        // open the dictionary file and read dictionary into an ArrayList
        Scanner input = new Scanner(new File(DICTIONARY_FILE));
        List<String> dictionary = new ArrayList<String>();
        while (input.hasNext()) {
            dictionary.add(input.next().toLowerCase());
        }

        // set up the AbsurdleManager and start the game
        List<String> dictionary2 = Collections.unmodifiableList(dictionary);
        AbsurdleManager absurdle = new AbsurdleManager(dictionary2, LENGTH);
        if (absurdle.words().isEmpty()) {
            System.out.println("No words of that length in the dictionary.");
        } else {
            Scanner console = new Scanner(System.in);
            List<String> patterns = new ArrayList<>();
            while (!isFinished(patterns)) {
                if (SHOW_COUNT) {
                    System.out.println(absurdle.words().size() + " words");
                }
                System.out.print("> ");
                String guess = console.next().toLowerCase().strip();
                String pattern = absurdle.record(guess);
                if (!pattern.isEmpty()) {
                    patterns.add(pattern);
                    System.out.println(": " + pattern);
                    System.out.println();
                }
            }
            System.out.println("Absurdle " + patterns.size() + "/∞");
            System.out.println();
            System.out.println(String.join("\n", patterns));
        }
    }

    private static boolean isFinished(List<String> patterns) {
        if (patterns.isEmpty()) {
            return false;
        }
        String lastPattern = patterns.get(patterns.size() - 1);
        return !lastPattern.contains("⬜") && !lastPattern.contains("🟨");
    }
}
