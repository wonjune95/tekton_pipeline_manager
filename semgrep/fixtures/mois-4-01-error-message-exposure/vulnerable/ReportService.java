package demo;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.jsp.JspWriter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ExceptionHandler;

// 탐지돼야 하는 경우 (진단가이드 4-1: 스택 트레이스·예외 메시지를 콘솔·응답으로 출력)
public class ReportService {
    private int reads;

    // ── 스택 트레이스 ──

    public String firstLine(String filename) {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            return rd.readLine();
        } catch (IOException e) {
            // 에러 메시지로 스택 정보가 노출됨
            // ruleid: mois-4-01-error-message-exposure
            e.printStackTrace();
            return "";
        }
    }

    // ── 콘솔 출력: System.out · System.err ──

    public String secondLine(String filename) {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            rd.readLine();
            return rd.readLine();
        } catch (IOException e) {
            // 오류 발생 시 화면에 출력된 시스템 정보가 다른 공격의 빌미가 된다
            // ruleid: mois-4-01-error-message-exposure
            System.err.print(e.getMessage());
            return "";
        }
    }

    // finally 가 붙은 try
    public int length(String filename) {
        try {
            return (int) new File(filename).length();
        } catch (SecurityException e) {
            // ruleid: mois-4-01-error-message-exposure
            System.out.println("실패: " + e);
            return 0;
        } finally {
            reads++;
        }
    }

    // catch 가 여러 개일 때 뒤쪽 catch
    public int parse(String filename) {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            return Integer.parseInt(rd.readLine());
        } catch (NumberFormatException nfe) {
            return 0;
        } catch (IOException ioe) {
            // ruleid: mois-4-01-error-message-exposure
            System.out.printf("실패: %s%n", ioe.getMessage());
            return -1;
        }
    }

    // ── HTTP 응답 출력: getWriter() 의 print·println·printf·format·write·append ──

    public void download(String filename, HttpServletResponse response) throws IOException {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            response.getWriter().println(rd.readLine());
        } catch (IOException e) {
            // ruleid: mois-4-01-error-message-exposure
            response.getWriter().println("오류: " + e);
            // ruleid: mois-4-01-error-message-exposure
            response.getWriter().print(e.getMessage());
            // ruleid: mois-4-01-error-message-exposure
            response.getWriter().printf("오류: %s", e.getMessage());
            // ruleid: mois-4-01-error-message-exposure
            response.getWriter().format("오류: %s", e);
            // ruleid: mois-4-01-error-message-exposure
            response.getWriter().write(e.toString());
            // ruleid: mois-4-01-error-message-exposure
            response.getWriter().append(e.getLocalizedMessage());
        }
    }

    // PrintWriter 변수에 담아 출력
    public void downloadByWriter(String filename, HttpServletResponse response) throws IOException {
        PrintWriter out = response.getWriter();
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            out.println(rd.readLine());
        } catch (IOException e) {
            // ruleid: mois-4-01-error-message-exposure
            out.println(e.getMessage());
        }
    }

    // JSP 출력 스트림
    public void render(String filename, JspWriter out) throws IOException {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            out.print(rd.readLine());
        } catch (IOException e) {
            // ruleid: mois-4-01-error-message-exposure
            out.print(e.getMessage());
        }
    }

    // 오류 응답 메시지
    public void head(String filename, HttpServletResponse response) throws IOException {
        try {
            response.setContentLength((int) new File(filename).length());
        } catch (SecurityException e) {
            // ruleid: mois-4-01-error-message-exposure
            response.sendError(500, e.getMessage());
        }
    }

    // ── Spring: 응답 본문·모델 ──

    public ResponseEntity<String> preview(String filename) {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            return ResponseEntity.ok(rd.readLine());
        } catch (IOException e) {
            // ruleid: mois-4-01-error-message-exposure
            return ResponseEntity.badRequest().body("읽기 실패: " + e.getMessage());
        }
    }

    public ResponseEntity<String> previewNew(String filename) {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            return ResponseEntity.ok(rd.readLine());
        } catch (IOException e) {
            // ruleid: mois-4-01-error-message-exposure
            return new ResponseEntity<>(e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    public String view(String filename, Model model) {
        try (BufferedReader rd = new BufferedReader(new FileReader(new File(filename)))) {
            model.addAttribute("line", rd.readLine());
            return "view";
        } catch (IOException e) {
            // ruleid: mois-4-01-error-message-exposure
            model.addAttribute("error", e.getMessage());
            return "error";
        }
    }

    // ── @ExceptionHandler 의 예외 인자 (try 밖) ──

    @ExceptionHandler(IllegalStateException.class)
    public ResponseEntity<String> handle(IllegalStateException e) {
        // ruleid: mois-4-01-error-message-exposure
        return ResponseEntity.status(500).body(e.getMessage());
    }

    @ExceptionHandler
    public ResponseEntity<String> handleIo(IOException ex) {
        // ruleid: mois-4-01-error-message-exposure
        return new ResponseEntity<String>(ex.toString(), HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
