package demo;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

// 탐지돼야 하는 경우: Spring 경로 변수를 그대로 파일 경로에 사용
@RestController
public class SpringFileController {
    private static final String BASE = "/data/uploads/";

    @GetMapping("/files/{name}")
    public byte[] download(@PathVariable String name) throws IOException {
        // ruleid: mois-1-03-path-traversal
        return Files.readAllBytes(Paths.get(BASE, name));
    }
}
