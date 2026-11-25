package demo;

import java.io.IOException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우 (진단가이드 6-2: J2EE 클래스에 남은 테스트용 main(), 콘솔 디버그 출력)
public class U489 extends HttpServlet {
    private int served;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) {
        // ruleid: mois-6-02-debug-code
        System.out.println("debug: " + request.getRequestURI());
        // ruleid: mois-6-02-debug-code
        System.err.printf("served=%d%n", served);
        response.setStatus(200);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) {
        try {
            response.getWriter().print("ok");
        } catch (IOException e) {
            // catch 안이라도 예외를 출력하는 것이 아니면 디버그 출력이다
            // ruleid: mois-6-02-debug-code
            System.out.println("응답 쓰기 실패");
            // (예외 자체를 출력하는 줄은 4-1 오류 메시지 정보노출 규칙이 맡는다 — 이 규칙으로는 표시하지 않음)
            System.err.println(e.getMessage());
        }
        try {
            response.flushBuffer();
        } catch (IOException e) {
            // ruleid: mois-6-02-debug-code
            System.err.print("flush 실패");
            // (finally 가 붙은 try 에서도 예외 출력은 4-1 이 맡는다)
            System.err.println("원인: " + e);
        } finally {
            served++;
        }
    }

    // 테스트를 위한 main() 함수가 남아 있다 (main 안의 출력은 따로 표시하지 않는다)
    // ruleid: mois-6-02-debug-code
    public static void main(String[] args) {
        System.err.printf("Print debug code");
    }
}

class BatchTool {
    // 가변 인자로 쓴 main
    // ruleid: mois-6-02-debug-code
    public static void main(String... args) {
        new BatchTool().toString();
    }
}
