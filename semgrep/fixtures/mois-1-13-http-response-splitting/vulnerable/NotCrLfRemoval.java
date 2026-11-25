package demo;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: CR·LF 를 지우는 것처럼 보이지만 실제로는 다른 글자를 지우거나, 지운 자리에 개행을 다시 넣는다
public class NotCrLfRemoval {
    // replace 는 정규식이 아니다: "\\r" 은 역슬래시와 r 두 글자라서 CR 문자는 그대로 남는다
    public void backslashLetters(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replace("\\r", "").replace("\\n", ""));
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replace("\\n", "").replace("\\r", ""));
        // ruleid: mois-1-13-http-response-splitting — 한쪽만 틀려도 같다
        response.setHeader("X-Value", v.replace("\\r", "").replace("\n", ""));
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replace("\r", "").replace("\\n", ""));
    }

    // 역슬래시 4개: 정규식 [\\r\\n] 은 역슬래시·r·n 세 글자의 집합이다
    public void escapedBackslashClass(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("[\\\\r\\\\n]", ""));
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("\\\\r|\\\\n", ""));
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("\\\\r", "").replaceAll("\\n", ""));
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("\\\\n", "").replaceAll("\\r", ""));
    }

    // 지운 자리에 개행을 다시 넣는다 (줄바꿈 통일, 헤더 접기)
    public void newlineReinserted(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("\\R", "\n"));
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("[\\r\\n]+", "\r\n "));
        // ruleid: mois-1-13-http-response-splitting — $1 은 지운 글자를 그대로 되돌린다
        response.setHeader("X-Value", v.replaceAll("(\\r|\\n)", "$1"));
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replace("\r", "").replace("\n", "\r"));
        // ruleid: mois-1-13-http-response-splitting — LF 를 CR·LF 로 바꾼 뒤 CR 만 지우면 LF 가 남는다
        response.setHeader("X-Value", v.replace("\n", "\r\n").replace("\r", ""));
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("\\r", "").replaceAll("\\n", "\r"));
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("\\n", "\r\n").replaceAll("\\r", ""));
    }

    // "\s" (역슬래시 1개)는 Java 15 부터 공백 한 글자다: 공백만 지운다
    public void spaceEscape(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("\s", ""));
    }

    // 문자 클래스 교집합: \r 과 \n 의 교집합은 비어 있다
    public void intersection(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("[\\r&&\\n]", ""));
    }
}
