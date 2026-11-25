package demo;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 탐지되면 안 되는 경우 (진단가이드 4-3 안전한 코드: 발생 가능한 예외를 나눠 처리, 반환값 확인)
public class DateReader {
    private static final Logger LOG = LoggerFactory.getLogger(DateReader.class);
    private int reads;

    public Date read(URL url) {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()))) {
            String line = reader.readLine();
            SimpleDateFormat format = new SimpleDateFormat("MM/dd/yy");
            return format.parse(line);
        // ok: mois-4-03-improper-exception-handling — 발생 가능한 예외를 하나씩 나눠 잡는다
        } catch (MalformedURLException e) {
            LOG.error("ERROR-11: 주소 오류");
        } catch (IOException e) {
            LOG.error("ERROR-12: 읽기 실패");
        } catch (ParseException e) {
            LOG.error("ERROR-13: 날짜 형식 오류");
        } finally {
            reads++;
        }
        return new Date(0L);
    }

    public int parseInt(String line) {
        try {
            return Integer.parseInt(line);
        // ok: mois-4-03-improper-exception-handling — RuntimeException 이 아니라 구체적인 하위 예외
        } catch (NumberFormatException e) {
            LOG.error("ERROR-15: 숫자 형식 오류");
            return 0;
        }
    }

    public void cleanUp(File tmp) throws IOException {
        // ok: mois-4-03-improper-exception-handling — 반환값을 확인해 실패를 알린다
        if (!tmp.delete()) {
            throw new IOException("ERROR-14: 임시 파일 삭제 실패");
        }
    }

    public boolean prepare(File dir) {
        // ok: mois-4-03-improper-exception-handling — 반환값을 변수에 받아 호출자에게 돌려준다
        boolean created = dir.mkdirs();
        return created || dir.isDirectory();
    }

    private boolean renamed;

    private static void requireTrue(boolean ok) throws IOException {
        if (!ok) {
            throw new IOException("ERROR-17");
        }
    }

    public boolean rotate(File log, File backup) throws IOException {
        // ok: mois-4-03-improper-exception-handling — 반환값을 필드에 대입·다른 호출의 인자로 전달·그대로 return
        renamed = log.renameTo(backup);
        requireTrue(backup.exists() || backup.createNewFile());
        LOG.info("ERROR-16: 이름 변경 결과 {}", Boolean.valueOf(backup.delete()));
        return log.delete();
    }
}
