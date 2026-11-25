package demo;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ExceptionHandler;

// 탐지되면 안 되는 경우 (진단가이드 4-1 안전한 코드: 오류 코드만 응답하고 상세 내용은 로거로 남김)
public class ReportService {
    private static final Logger LOG = LoggerFactory.getLogger(ReportService.class);

    public String firstLine(String filename) {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            return rd.readLine();
        } catch (IOException e) {
            // ok: mois-4-01-error-message-exposure — 예외는 로거로만 남긴다
            LOG.error("ERROR-01: 파일 열기 에러", e);
            return "";
        }
    }

    public void download(String filename, HttpServletResponse response) throws IOException {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            response.getWriter().println(rd.readLine());
        } catch (IOException e) {
            LOG.error("ERROR-02: 다운로드 실패", e);
            // ok: mois-4-01-error-message-exposure — 응답에는 정해진 오류 코드만 쓴다 (예외 변수를 쓰지 않음)
            response.sendError(500, "ERROR-02");
            response.getWriter().println("ERROR-02: 요청을 처리하지 못했습니다");
        }
    }

    public String view(String filename, Model model) {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            model.addAttribute("line", rd.readLine());
            return "view";
        } catch (IOException e) {
            LOG.error("ERROR-04: 미리보기 실패", e);
            // ok: mois-4-01-error-message-exposure — 모델에는 오류 코드만 담는다
            model.addAttribute("error", "ERROR-04");
            return "error";
        }
    }

    @ExceptionHandler(IllegalStateException.class)
    public ResponseEntity<String> handle(IllegalStateException e) {
        LOG.error("ERROR-03", e);
        // ok: mois-4-01-error-message-exposure — 본문은 고정 문자열
        return ResponseEntity.status(500).body("ERROR-03");
    }

    @ExceptionHandler
    public ResponseEntity<String> handleIo(IOException e) {
        LOG.error("ERROR-05", e);
        // ok: mois-4-01-error-message-exposure — 본문은 고정 문자열
        return new ResponseEntity<>("ERROR-05", HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
