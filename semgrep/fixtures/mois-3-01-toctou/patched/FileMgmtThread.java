package demo;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Path;
import java.nio.file.Paths;

// 탐지되면 안 되는 경우 (진단가이드 3-1 안전한 코드: 검사와 사용을 같은 잠금 안에서 수행)
class FileMgmtThread extends Thread {
    private static final Object SYNC = new Object();
    private final String manageType;

    FileMgmtThread(String type) {
        manageType = type;
    }

    @Override
    public void run() {
        // ok: mois-3-01-toctou — 검사(if)와 사용이 같은 synchronized 블록 안에 있다
        synchronized (SYNC) {
            try {
                if (manageType.equals("READ")) {
                    File f = new File("Test_367.txt");
                    if (f.exists()) {
                        try (BufferedReader br = new BufferedReader(new FileReader(f))) {
                            br.readLine();
                        }
                    }
                } else if (manageType.equals("DELETE")) {
                    File f = new File("Test_367.txt");
                    if (f.exists() && !f.delete()) {
                        throw new IOException("삭제 실패: " + f.getName());
                    }
                }
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        }
    }

    // ok: mois-3-01-toctou — synchronized 메서드 안에서 검사하고 사용한다
    synchronized void removeIfPresent(Path p) throws IOException {
        if (Files.exists(p)) {
            Files.delete(p);
        }
    }

    // ok: mois-3-01-toctou — java.io.File 도 synchronized 메서드 안이면 같다
    synchronized void removeIfPresent(File f) throws IOException {
        if (f.exists() && !f.delete()) {
            throw new IOException("삭제 실패: " + f.getName());
        }
    }

    // ok: mois-3-01-toctou — NIO 검사와 사용이 같은 synchronized 블록 안에 있다
    byte[] readLocked(Path p) throws IOException {
        synchronized (SYNC) {
            if (Files.isReadable(p)) {
                return Files.readAllBytes(p);
            }
        }
        return new byte[0];
    }

    // ok: mois-3-01-toctou — 검사 없이 바로 열고, 없으면 예외로 처리한다
    byte[] read() throws IOException {
        try {
            return Files.readAllBytes(Paths.get("Test_367.txt"));
        } catch (NoSuchFileException e) {
            return new byte[0];
        }
    }

    // ok: mois-3-01-toctou — 검사한 파일(lock)과 여는 파일(data)이 다르다
    int readUnlessLocked(File lock, File data) throws IOException {
        if (!lock.exists()) {
            try (FileReader r = new FileReader(data)) {
                return r.read();
            }
        }
        return -1;
    }
}
