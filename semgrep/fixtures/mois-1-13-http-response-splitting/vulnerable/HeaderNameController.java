package demo;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.http.HttpHeaders;

// 탐지돼야 하는 경우: 외부 입력이 헤더 "이름" 자리에 들어간다 (값 자리와 똑같이 CR·LF 로 응답이 나뉜다)
public class HeaderNameController {
    public void custom(HttpServletRequest request, HttpServletResponse response) {
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader(request.getParameter("name"), "1");
    }

    public HttpHeaders spring(HttpServletRequest request) {
        HttpHeaders headers = new HttpHeaders();
        // ruleid: mois-1-13-http-response-splitting
        headers.add(request.getParameter("name"), "1");
        // ruleid: mois-1-13-http-response-splitting
        headers.set(request.getParameter("other"), "1");
        return headers;
    }
}
