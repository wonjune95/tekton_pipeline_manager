package demo;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

// 탐지돼야 하는 경우: 예외를 잡고 아무것도 하지 않음 (탐지 위치는 try 줄)
public class Loader {
    private int loaded;

    public List<String> load(String path) {
        // ruleid: mois-4-02-empty-catch
        try {
            return Files.readAllLines(Paths.get(path));
        } catch (IOException e) {
        }
        return null;
    }

    // finally 가 있어도 catch 가 비어 있으면 같다
    public List<String> loadWithFinally(String path) {
        // ruleid: mois-4-02-empty-catch
        try {
            return Files.readAllLines(Paths.get(path));
        } catch (IOException e) {
        } finally {
            loaded++;
        }
        return null;
    }

    // try-with-resources
    public String firstLine(String path) {
        // ruleid: mois-4-02-empty-catch
        try (BufferedReader br = Files.newBufferedReader(Paths.get(path))) {
            return br.readLine();
        } catch (IOException e) {
        }
        return null;
    }

    // try-with-resources + finally
    public String firstLineWithFinally(String path) {
        // ruleid: mois-4-02-empty-catch
        try (BufferedReader br = Files.newBufferedReader(Paths.get(path))) {
            return br.readLine();
        } catch (IOException e) {
        } finally {
            loaded++;
        }
        return null;
    }

    // catch 가 여러 개일 때 그중 하나만 비어 있어도 탐지 (앞·뒤 어느 쪽이든)
    public int parseSecond(String path) {
        // ruleid: mois-4-02-empty-catch
        try {
            return Integer.parseInt(Files.readAllLines(Paths.get(path)).get(1));
        } catch (NumberFormatException e) {
            loaded = -1;
        } catch (IOException e) {
        }
        return 0;
    }

    public int parseFirst(String path) {
        // ruleid: mois-4-02-empty-catch
        try {
            return Integer.parseInt(Files.readAllLines(Paths.get(path)).get(0));
        } catch (NumberFormatException e) {
        } catch (IOException e) {
            loaded = -1;
        }
        return 0;
    }

    // 다중 타입 catch, 주석만 있는 catch
    public int parseAny(String path) {
        // ruleid: mois-4-02-empty-catch
        try {
            return Integer.parseInt(Files.readAllLines(Paths.get(path)).get(0));
        } catch (NumberFormatException | IOException e) {
            // 무시
        }
        return 0;
    }
}
