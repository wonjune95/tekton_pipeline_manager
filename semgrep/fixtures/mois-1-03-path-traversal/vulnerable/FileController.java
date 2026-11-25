package demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import javax.servlet.http.HttpServletRequest;

// 탐지돼야 하는 경우: 외부 입력을 그대로 파일 경로에 사용 (../ 로 상위 디렉터리 접근 가능). sink 마다 한 줄씩
public class FileController {
    private static final String BASE = "/data/uploads/";
    private final Path baseDir = Paths.get(BASE);

    public byte[] download(HttpServletRequest request) throws IOException {
        String name = request.getParameter("file");
        // ruleid: mois-1-03-path-traversal
        return Files.readAllBytes(Paths.get(BASE + name));
    }

    public FileInputStream open(HttpServletRequest request) throws IOException {
        String path = request.getParameter("path");
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(new File(BASE, path));
    }

    public File file(HttpServletRequest request) {
        // ruleid: mois-1-03-path-traversal
        return new File(BASE + request.getParameter("file"));
    }

    public FileInputStream input(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(BASE + request.getParameter("file"));
    }

    public FileOutputStream output(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        return new FileOutputStream(BASE + request.getParameter("file"));
    }

    public FileReader reader(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        return new FileReader(BASE + request.getParameter("file"));
    }

    public FileWriter writer(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        return new FileWriter(BASE + request.getParameter("file"));
    }

    public Path of(HttpServletRequest request) {
        // ruleid: mois-1-03-path-traversal
        return Path.of(BASE, request.getParameter("file"));
    }

    // 기준 디렉터리에 입력을 이어 붙여도 ../ 는 그대로 남는다
    public byte[] resolve(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        return Files.readAllBytes(baseDir.resolve(request.getParameter("file")));
    }

    public Path resolveFromGet(HttpServletRequest request) {
        // ruleid: mois-1-03-path-traversal
        return Paths.get(BASE).resolve(request.getParameter("file"));
    }

    public Path resolveFromOf(HttpServletRequest request) {
        // ruleid: mois-1-03-path-traversal
        return Path.of(BASE).resolve(request.getParameter("file"));
    }

    public Path sibling(HttpServletRequest request) {
        // ruleid: mois-1-03-path-traversal
        return baseDir.resolveSibling(request.getParameter("file"));
    }
}
