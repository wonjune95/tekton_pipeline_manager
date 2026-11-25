package demo;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 탐지되면 안 되는 경우: 잡은 예외를 처리함 (다시 던짐·기록·대체값)
public class Loader {
    private static final Logger LOG = LoggerFactory.getLogger(Loader.class);
    private int loaded;

    public List<String> load(String path) {
        try {
            return Files.readAllLines(Paths.get(path));
        } catch (IOException e) {
            // ok: mois-4-02-empty-catch — 호출자가 처리하도록 다시 던진다
            throw new UncheckedIOException(e);
        }
    }

    public String firstLine(String path) {
        try (BufferedReader br = Files.newBufferedReader(Paths.get(path))) {
            return br.readLine();
        } catch (IOException e) {
            // ok: mois-4-02-empty-catch — 오류 코드를 기록하고 대체값을 돌려준다
            LOG.error("ERROR-30: 파일 읽기 실패");
            return "";
        } finally {
            loaded++;
        }
    }

    // ok: mois-4-02-empty-catch — catch 없이 finally 만 있는 try
    public List<String> loadCounting(String path) throws IOException {
        try {
            return Files.readAllLines(Paths.get(path));
        } finally {
            loaded++;
        }
    }
}
