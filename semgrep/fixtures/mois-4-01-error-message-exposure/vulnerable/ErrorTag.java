package demo;

import jakarta.servlet.jsp.JspWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

// 탐지돼야 하는 경우: jakarta 네임스페이스의 JSP 출력 스트림에 예외 메시지를 씀
public class ErrorTag {
    public void render(String filename, JspWriter out) throws IOException {
        try {
            out.print(Files.size(Paths.get(filename)));
        } catch (IOException e) {
            // ruleid: mois-4-01-error-message-exposure
            out.println(e.getMessage());
        }
    }
}
