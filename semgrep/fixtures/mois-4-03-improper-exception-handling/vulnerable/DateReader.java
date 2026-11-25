package demo;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 탐지돼야 하는 경우 (진단가이드 4-3: 광범위한 Exception 처리, 반환값 미검사)
public class DateReader {
    private static final Logger LOG = LoggerFactory.getLogger(DateReader.class);
    private int reads;

    // ── 광범위한 예외: Exception · Throwable · RuntimeException (탐지 위치는 catch 의 타입) ──

    public Date read(URL url) {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()))) {
            String line = reader.readLine();
            SimpleDateFormat format = new SimpleDateFormat("MM/dd/yy");
            return format.parse(line);
        // ruleid: mois-4-03-improper-exception-handling
        } catch (Exception e) {
            // 예외를 세분화할 수 있는데도 광범위하게 처리한다
            LOG.error("ERROR-10: 날짜 읽기 실패");
            return null;
        }
    }

    public Date parse(String line) {
        try {
            return new SimpleDateFormat("MM/dd/yy").parse(line);
        // ruleid: mois-4-03-improper-exception-handling
        } catch (Throwable t) {
            LOG.error("ERROR-10: 날짜 읽기 실패");
            return null;
        }
    }

    public int parseInt(String line) {
        try {
            return Integer.parseInt(line);
        // ruleid: mois-4-03-improper-exception-handling
        } catch (RuntimeException e) {
            LOG.error("ERROR-10: 숫자 읽기 실패");
            return 0;
        }
    }

    // 전체 이름, final 이 붙은 형태
    public int parseQualified(String line) {
        try {
            return Integer.parseInt(line);
        // ruleid: mois-4-03-improper-exception-handling
        } catch (final java.lang.Exception e) {
            LOG.error("ERROR-10: 숫자 읽기 실패");
            return 0;
        }
    }

    // finally 가 붙은 try
    public int parseCounting(String line) {
        try {
            return Integer.parseInt(line);
        // ruleid: mois-4-03-improper-exception-handling
        } catch (Exception e) {
            LOG.error("ERROR-10: 숫자 읽기 실패");
            return 0;
        } finally {
            reads++;
        }
    }

    // try-with-resources + finally
    public String firstLine(URL url) {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()))) {
            return reader.readLine();
        // ruleid: mois-4-03-improper-exception-handling
        } catch (Exception e) {
            LOG.error("ERROR-12: 읽기 실패");
            return "";
        } finally {
            reads++;
        }
    }

    // 구체적인 예외를 먼저 잡았어도 뒤에서 Exception 으로 뭉뚱그리면 탐지
    public String secondLine(URL url) {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()))) {
            reader.readLine();
            return reader.readLine();
        } catch (IOException e) {
            LOG.error("ERROR-12: 읽기 실패");
            return "";
        // ruleid: mois-4-03-improper-exception-handling
        } catch (Exception e) {
            LOG.error("ERROR-19: 알 수 없는 오류");
            return "";
        }
    }

    // ── 실패를 boolean 으로 알리는 java.io.File API 의 반환값을 버림 ──

    public void cleanUp(File tmp) {
        // 삭제 실패를 알 수 없다
        // ruleid: mois-4-03-improper-exception-handling
        tmp.delete();
    }

    public void prepare(File dir, File marker, File old) throws IOException {
        // ruleid: mois-4-03-improper-exception-handling
        dir.mkdir();
        // ruleid: mois-4-03-improper-exception-handling
        dir.mkdirs();
        // ruleid: mois-4-03-improper-exception-handling
        marker.createNewFile();
        // ruleid: mois-4-03-improper-exception-handling
        old.renameTo(new File(dir, "old.bak"));
    }

    // if 본문·람다 본문 안의 문장도 같다
    public void cleanAll(java.util.List<File> files, boolean force) {
        if (force) {
            // ruleid: mois-4-03-improper-exception-handling
            files.get(0).delete();
        }
        files.forEach((File f) -> {
            // ruleid: mois-4-03-improper-exception-handling
            f.delete();
        });
    }
}
