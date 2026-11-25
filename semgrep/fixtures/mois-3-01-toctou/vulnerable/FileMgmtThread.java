package demo;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

// 탐지돼야 하는 경우 (진단가이드 3-1 안전하지 않은 코드: 파일 존재 검사 후 동기화 없이 읽기·삭제)
class FileMgmtThread extends Thread {
    private static final Object SYNC = new Object();
    private final String manageType;

    FileMgmtThread(String type) {
        manageType = type;
    }

    @Override
    public void run() {
        try {
            if (manageType.equals("READ")) {
                File f = new File("Test_367.txt");
                if (f.exists()) {
                    // ruleid: mois-3-01-toctou
                    BufferedReader br = new BufferedReader(new FileReader(f));
                    br.close();
                }
            } else if (manageType.equals("DELETE")) {
                File f = new File("Test_367.txt");
                if (f.exists()) {
                    // ruleid: mois-3-01-toctou
                    f.delete();
                }
            }
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    // ── java.io.File: 검사 4종(exists·canRead·canWrite·isFile) × 사용(스트림 5종, delete·renameTo·createNewFile) ──

    int readByte(File f) throws IOException {
        if (f.canRead()) {
            // ruleid: mois-3-01-toctou
            try (FileInputStream in = new FileInputStream(f)) {
                return in.read();
            }
        }
        return -1;
    }

    void overwrite(File f) throws IOException {
        if (f.canWrite()) {
            // ruleid: mois-3-01-toctou
            try (FileOutputStream out = new FileOutputStream(f, false)) {
                out.write(0);
            }
        }
    }

    void append(File f) throws IOException {
        if (f.isFile()) {
            // ruleid: mois-3-01-toctou
            try (FileWriter w = new FileWriter(f, true)) {
                w.write("x");
            }
        }
    }

    long length(File f) throws IOException {
        if (f.exists() && f.isFile()) {
            // ruleid: mois-3-01-toctou
            try (RandomAccessFile raf = new RandomAccessFile(f, "r")) {
                return raf.length();
            }
        }
        return 0L;
    }

    // 전체 이름으로 쓴 스트림
    int readQualified(File f) throws IOException {
        if (f.exists()) {
            // ruleid: mois-3-01-toctou
            try (java.io.FileReader r = new java.io.FileReader(f)) {
                return r.read();
            }
        }
        return -1;
    }

    boolean rotate(File f, File backup) {
        if (f.exists()) {
            // ruleid: mois-3-01-toctou
            return f.renameTo(backup);
        }
        return false;
    }

    // 없을 때만 만든다: 검사와 생성 사이에 다른 스레드가 먼저 만들 수 있다
    void createOnce(File f) throws IOException {
        if (!f.exists()) {
            // ruleid: mois-3-01-toctou
            f.createNewFile();
        }
    }

    // 조건식 안에서 바로 사용
    boolean deleteInCondition(File f) {
        // ruleid: mois-3-01-toctou
        if (f.exists() && !f.delete()) {
            return false;
        }
        return true;
    }

    // else 쪽에서 사용
    int readInElse(File f) throws IOException {
        if (!f.canRead()) {
            return -1;
        } else {
            // ruleid: mois-3-01-toctou
            try (FileInputStream in = new FileInputStream(f)) {
                return in.read();
            }
        }
    }

    // 사용만 잠금 안에 있고 검사는 잠금 밖에 있다 → 검사와 사용이 묶이지 않는다
    void lockOnlyAroundUse(File f) {
        if (f.exists()) {
            synchronized (SYNC) {
                // ruleid: mois-3-01-toctou
                f.delete();
            }
        }
    }

    // ── java.nio.file.Files: 검사 5종 × 사용 12종 ──

    // NIO 도 같음: 존재 검사 후 다른 스레드가 지울 수 있다
    byte[] readIfPresent() throws IOException {
        Path p = Paths.get("Test_367.txt");
        if (Files.exists(p)) {
            // ruleid: mois-3-01-toctou
            return Files.readAllBytes(p);
        }
        return new byte[0];
    }

    void nioCreate(Path p) throws IOException {
        if (Files.notExists(p)) {
            // ruleid: mois-3-01-toctou
            Files.createFile(p);
        }
    }

    List<String> nioLines(Path p) throws IOException {
        if (Files.isReadable(p)) {
            // ruleid: mois-3-01-toctou
            return Files.readAllLines(p);
        }
        return List.of();
    }

    void nioWrite(Path p, byte[] data) throws IOException {
        if (Files.isWritable(p)) {
            // ruleid: mois-3-01-toctou
            Files.write(p, data);
        }
    }

    void nioDelete(Path p) throws IOException {
        if (Files.isRegularFile(p)) {
            // ruleid: mois-3-01-toctou
            Files.delete(p);
        }
    }

    void nioDeleteIfExists(Path p) throws IOException {
        if (Files.isRegularFile(p)) {
            // ruleid: mois-3-01-toctou
            Files.deleteIfExists(p);
        }
    }

    void nioMoveCopy(Path p, Path target, Path backup) throws IOException {
        if (Files.exists(p)) {
            // ruleid: mois-3-01-toctou
            Files.copy(p, backup);
            // ruleid: mois-3-01-toctou
            Files.move(p, target);
        }
    }

    void nioStreams(Path p) throws IOException {
        if (Files.exists(p)) {
            // ruleid: mois-3-01-toctou
            Files.newInputStream(p).close();
            // ruleid: mois-3-01-toctou
            Files.newOutputStream(p).close();
            // ruleid: mois-3-01-toctou
            Files.newBufferedReader(p).close();
            // ruleid: mois-3-01-toctou
            Files.newBufferedWriter(p, StandardCharsets.UTF_8).close();
        }
    }

    // 사용만 잠금 안에 있다
    void nioLockOnlyAroundUse(Path p) throws IOException {
        if (Files.exists(p)) {
            synchronized (SYNC) {
                // ruleid: mois-3-01-toctou
                Files.delete(p);
            }
        }
    }
}
