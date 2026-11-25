package demo;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;
import javax.servlet.http.HttpServletRequest;
import org.apache.commons.io.FileUtils;

// 탐지돼야 하는 경우: 경로 검사는 맞게 썼지만, 검사하기 전에 그 File 을 다른 호출·생성자에 넘겨 이미 읽었다
// (File 을 만드는 줄이 탐지된다. 검사 뒤의 사용은 안전하므로 탐지되지 않는다)
public class UsedBeforeGuardController {
    private static final String BASE = "/data/upload";

    public byte[] readByUtilityBeforeCheck(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("name"));
        byte[] data = FileUtils.readFileToByteArray(f);
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        return data;
    }

    public String openedByConstructorBeforeCheck(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("name"));
        Scanner sc = new Scanner(f);
        String first = sc.nextLine();
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        return first;
    }
}
