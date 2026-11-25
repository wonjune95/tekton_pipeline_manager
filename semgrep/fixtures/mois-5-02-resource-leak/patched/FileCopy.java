package demo;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.support.JdbcUtils;

// 탐지되면 안 되는 경우 (진단가이드 5-2 안전한 코드: finally 에서 해제, try-with-resources, 자원을 돌려주는 함수)
public class FileCopy {
    private static final Logger LOG = LoggerFactory.getLogger(FileCopy.class);
    private InputStream current = null;
    private int opened;

    // ── finally 에서 닫음 ──

    public void copy(String inputFile, String outputFile) {
        InputStream in = null;
        OutputStream out = null;
        try {
            in = new FileInputStream(inputFile);
            out = new FileOutputStream(outputFile);
            in.transferTo(out);
        } catch (IOException e) {
            LOG.error("ERROR-20: 복사 실패");
        } finally {
            // ok: mois-5-02-resource-leak — 항상 수행되는 finally 에서 각 자원을 null 검사 후 해제
            if (in != null) {
                try {
                    in.close();
                } catch (IOException e) {
                    LOG.error("ERROR-21: 해제 실패");
                }
            }
            if (out != null) {
                try {
                    out.close();
                } catch (IOException e) {
                    LOG.error("ERROR-21: 해제 실패");
                }
            }
        }
    }

    // ok: mois-5-02-resource-leak — try 안에서 열고 finally 에서 닫음 (catch 없음)
    public int firstByte(String path) throws IOException {
        InputStream in = null;
        try {
            in = new FileInputStream(path);
            return in.read();
        } finally {
            if (in != null) {
                in.close();
            }
        }
    }

    // ok: mois-5-02-resource-leak — try 앞에서 열고 바로 뒤 try 의 finally 에서 닫음
    public int count(String url, String user, String pass) throws SQLException {
        Connection conn = DriverManager.getConnection(url, user, pass);
        try {
            return conn.getNetworkTimeout();
        } finally {
            conn.close();
        }
    }

    public int countLogged(String url, String user, String pass) throws SQLException {
        Connection conn = DriverManager.getConnection(url, user, pass);
        try {
            return conn.getNetworkTimeout();
        } catch (SQLException e) {
            LOG.error("ERROR-22: 조회 실패");
            throw e;
        } finally {
            // ok: mois-5-02-resource-leak — catch 가 있어도 finally 에서 닫음
            conn.close();
        }
    }

    // ── finally 에서 해제 함수에 넘김 ──

    public int byCloser(String path) throws IOException {
        InputStream in = null;
        try {
            in = new FileInputStream(path);
            return in.read();
        } finally {
            // ok: mois-5-02-resource-leak — 해제 함수(closeQuietly)에 같은 자원을 넘김
            IOUtils.closeQuietly(in);
        }
    }

    public int byCloserWithCatch(String path) {
        InputStream in = null;
        try {
            in = Files.newInputStream(Path.of(path));
            return in.read();
        } catch (IOException e) {
            LOG.error("ERROR-23: 읽기 실패");
            return -1;
        } finally {
            // ok: mois-5-02-resource-leak — 같은 클래스의 해제 함수
            closeAll(in);
        }
    }

    public int byCloserAfterOpen(String url, String user, String pass) throws SQLException {
        Connection conn = DriverManager.getConnection(url, user, pass);
        try {
            return conn.getNetworkTimeout();
        } finally {
            // ok: mois-5-02-resource-leak — try 앞에서 열고 finally 에서 해제 함수에 넘김
            JdbcUtils.closeConnection(conn);
        }
    }

    public int byReleaseAfterOpen(String url, String user, String pass) {
        Connection conn = null;
        conn = openOrNull(url, user, pass);
        InputStream in = Files.newInputStream(Path.of(url));
        try {
            return in.read() + conn.getNetworkTimeout();
        } catch (IOException | SQLException e) {
            LOG.error("ERROR-24: 조회 실패");
            return -1;
        } finally {
            // ok: mois-5-02-resource-leak — 이름에 release 가 들어간 해제 함수
            releaseQuietly(in);
            JdbcUtils.closeConnection(conn);
        }
    }

    // ── try-with-resources ──

    public String firstLine(String path) throws IOException {
        // ok: mois-5-02-resource-leak — try-with-resources
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            return br.readLine();
        }
    }

    public String firstLineOrEmpty(String path) {
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            return br.readLine();
        } catch (IOException e) {
            LOG.error("ERROR-25: 읽기 실패");
            return "";
        }
    }

    public String firstLineCounting(String path) throws IOException {
        try (BufferedReader br = Files.newBufferedReader(Path.of(path))) {
            return br.readLine();
        } finally {
            opened++;
        }
    }

    public String firstLineCountingOrEmpty(String path) {
        try (BufferedReader br = Files.newBufferedReader(Path.of(path))) {
            return br.readLine();
        } catch (IOException e) {
            LOG.error("ERROR-25: 읽기 실패");
            return "";
        } finally {
            opened++;
        }
    }

    // ── 자원을 돌려주거나 필드에 넘김: 해제는 받는 쪽 몫 (오탐 예) ──

    public static Connection open(String url, String user, String pass) throws SQLException {
        // ok: mois-5-02-resource-leak — 자원을 돌려주는 함수는 호출한 쪽이 해제한다
        Connection conn = DriverManager.getConnection(url, user, pass);
        return conn;
    }

    public void attach(String path) throws IOException {
        // ok: mois-5-02-resource-leak — 필드에 넘겨 객체가 수명을 관리한다 (close() 에서 해제)
        InputStream in = new FileInputStream(path);
        this.current = in;
    }

    public void reopen(String path) throws IOException {
        close();
        // ok: mois-5-02-resource-leak — 지역 변수가 아니라 필드에 직접 대입 (객체가 수명을 관리)
        current = new FileInputStream(path);
    }

    public void close() throws IOException {
        if (current != null) {
            current.close();
        }
    }

    private static Connection openOrNull(String url, String user, String pass) {
        try {
            return DriverManager.getConnection(url, user, pass);
        } catch (SQLException e) {
            return null;
        }
    }

    private static void closeAll(InputStream in) {
        IOUtils.closeQuietly(in);
    }

    private static void releaseQuietly(InputStream in) {
        IOUtils.closeQuietly(in);
    }
}
