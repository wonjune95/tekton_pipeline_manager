package demo;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: 치환은 하지만 CR·LF 가 남는 형태
public class NotStrippedController {
    // \r\n 쌍만 지움: \n 하나만 넣으면 그대로 남는다
    public void pairOnly(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("\\r\\n", ""));
    }

    // \n 과 \r\n 만 지움: \r 하나는 남는다
    public void optionalCr(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("\\r?\\n", ""));
    }

    // 한쪽만 지움
    public void crOnly(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replace("\r", ""));
    }

    public void crClassOnly(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("[\\r]", ""));
    }

    public void lfClassOnly(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("[\\n\\t]", ""));
    }

    // 이어서 지우지만 \n 이 아닌 다른 문자
    public void crAndTab(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replace("\r", "").replace("\t", ""));
    }

    // 부정 문자 클래스: CR·LF 만 남기고 나머지를 지운다
    public void negatedClass(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replaceAll("[^\\r\\n]", ""));
    }

    // 개행과 무관한 치환
    public void unrelated(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.replace(" ", "").replaceAll("<", "&lt;"));
    }

    // 앞뒤 공백만 지움: 가운데 있는 개행은 남는다
    public void trimOnly(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v.trim());
    }

    // 치환 결과를 쓰지 않음 (String 은 바뀌지 않는다)
    public void resultIgnored(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        v.replaceAll("[\\r\\n]", "");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Value", v);
    }

    // 다른 변수를 치환
    public void otherVariable(HttpServletRequest request, HttpServletResponse response) {
        String v = request.getParameter("v");
        String label = "value".replaceAll("[\\r\\n]", "");
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-" + label, v);
    }
}
