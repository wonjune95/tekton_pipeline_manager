package demo;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.RandomAccessFile;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.jar.JarFile;
import java.util.zip.ZipFile;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 탐지돼야 하는 경우 (진단가이드 5-2: try 안에서 닫아 예외가 나면 자원이 반환되지 않음)
public class FileCopy {
    private static final Logger LOG = LoggerFactory.getLogger(FileCopy.class);

    // ── 대입 형태: 먼저 선언하고 try 안에서 연다 ──

    public void copy(String inputFile, String outputFile) {
        InputStream in = null;
        OutputStream out = null;
        try {
            // ruleid: mois-5-02-resource-leak
            in = new FileInputStream(inputFile);
            // ruleid: mois-5-02-resource-leak
            out = new FileOutputStream(outputFile);
            in.transferTo(out);
            // 자원 반환 전에 오류가 나면 반환되지 않는다
            in.close();
            out.close();
        } catch (IOException e) {
            LOG.error("ERROR-20: 복사 실패");
        }
    }

    // ── 선언 형태: 파일 스트림 7종 (감싼 스트림 포함) ──

    public String firstLine(String path) throws IOException {
        // ruleid: mois-5-02-resource-leak
        BufferedReader br = new BufferedReader(new FileReader(path));
        return br.readLine();
    }

    public void appendLine(String path, String line) throws IOException {
        // ruleid: mois-5-02-resource-leak
        FileWriter w = new FileWriter(path, true);
        w.write(line);
        w.close();
    }

    public long length(String path) throws IOException {
        // ruleid: mois-5-02-resource-leak
        RandomAccessFile raf = new RandomAccessFile(path, "r");
        return raf.length();
    }

    public int entries(String path) throws IOException {
        // ruleid: mois-5-02-resource-leak
        ZipFile zip = new ZipFile(path);
        // ruleid: mois-5-02-resource-leak
        JarFile jar = new JarFile(path);
        return zip.size() + jar.size();
    }

    // 전체 이름으로 쓴 클래스
    public int firstByte(String path) throws IOException {
        // ruleid: mois-5-02-resource-leak
        java.io.InputStream in = new java.io.FileInputStream(path);
        // ruleid: mois-5-02-resource-leak
        java.util.zip.ZipFile zip = new java.util.zip.ZipFile(path);
        // ruleid: mois-5-02-resource-leak
        java.util.jar.JarFile jar = new java.util.jar.JarFile(path);
        return in.read() + zip.size() + jar.size();
    }

    // ── DriverManager 연결: 선언·대입 ──

    public int count(String url, String user, String pass) throws SQLException {
        // ruleid: mois-5-02-resource-leak
        Connection conn = DriverManager.getConnection(url, user, pass);
        return conn.getNetworkTimeout();
    }

    public int countLate(String url, String user, String pass) throws SQLException {
        Connection conn = null;
        // ruleid: mois-5-02-resource-leak
        conn = DriverManager.getConnection(url, user, pass);
        return conn.getNetworkTimeout();
    }

    // ── NIO 스트림 4종 ──

    public void nio(Path src, Path dst) throws IOException {
        // ruleid: mois-5-02-resource-leak
        InputStream in = Files.newInputStream(src);
        // ruleid: mois-5-02-resource-leak
        OutputStream out = Files.newOutputStream(dst);
        in.transferTo(out);
        // ruleid: mois-5-02-resource-leak
        BufferedReader reader = Files.newBufferedReader(src);
        // ruleid: mois-5-02-resource-leak
        BufferedWriter writer = Files.newBufferedWriter(dst);
        writer.write(reader.readLine());
    }

    // ── 해제처럼 보이지만 이 자원은 해제되지 않는 경우 ──

    // finally 에서 다른 자원(out)만 닫는다
    public void closesOther(String inputFile, String outputFile) throws IOException {
        InputStream in = null;
        OutputStream out = null;
        try {
            // ruleid: mois-5-02-resource-leak
            in = new FileInputStream(inputFile);
            out = new FileOutputStream(outputFile);
            in.transferTo(out);
        } finally {
            if (out != null) {
                out.close();
            }
        }
    }

    // finally 에서 자원을 로그 함수에 넘길 뿐 닫지 않는다
    public int loggedOnly(String path) throws IOException {
        InputStream in = null;
        try {
            // ruleid: mois-5-02-resource-leak
            in = new FileInputStream(path);
            return in.read();
        } finally {
            LOG.info("읽기 끝: {}", in);
        }
    }

    // catch 에서만 닫는다 (정상 흐름에서는 닫히지 않음)
    public int closedInCatchOnly(String path) throws IOException {
        InputStream in = null;
        try {
            // ruleid: mois-5-02-resource-leak
            in = new FileInputStream(path);
            return in.read();
        } catch (IOException e) {
            in.close();
            throw e;
        }
    }

    // try-with-resources 가 관리하는 것은 out 뿐이다
    public void otherResourceManaged(String inputFile, String outputFile) throws IOException {
        try (OutputStream out = new FileOutputStream(outputFile)) {
            // ruleid: mois-5-02-resource-leak
            InputStream in = new FileInputStream(inputFile);
            in.transferTo(out);
        }
    }
}
