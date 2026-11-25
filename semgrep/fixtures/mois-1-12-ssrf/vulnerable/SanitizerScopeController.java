package demo;

import javax.servlet.http.HttpServletRequest;
import org.springframework.web.client.RestTemplate;

// 탐지돼야 하는 경우: 안전해 보이는 식(숫자 변환, 고정 주소로 시작하는 문자열) 안이나 뒤에서 입력이 요청 대상을 정한다
public class SanitizerScopeController {
    private final RestTemplate restTemplate = new RestTemplate();

    // 숫자로 바꾸는 것은 응답이고, 요청은 입력한 주소로 이미 나갔다
    public int countFromIntResponse(HttpServletRequest request) {
        String url = request.getParameter("url");
        // ruleid: mois-1-12-ssrf
        return Integer.parseInt(restTemplate.getForObject(url, String.class));
    }

    public int countFromIntVariable(HttpServletRequest request) {
        String url = request.getParameter("url");
        // ruleid: mois-1-12-ssrf
        int count = Integer.parseInt(restTemplate.getForObject(url, String.class));
        return count;
    }

    public long countFromLongResponse(HttpServletRequest request) {
        String url = request.getParameter("url");
        // ruleid: mois-1-12-ssrf
        return Long.parseLong(restTemplate.getForObject(url, String.class));
    }

    public long countFromLongVariable(HttpServletRequest request) {
        String url = request.getParameter("url");
        // ruleid: mois-1-12-ssrf
        long count = Long.parseLong(restTemplate.getForObject(url, String.class));
        return count;
    }

    // 바깥 요청은 고정 주소지만, 이어 붙이는 값을 얻으려고 입력한 주소로 먼저 요청한다
    public String tokenFromInputUrl(HttpServletRequest request) {
        String tokenUrl = request.getParameter("tokenUrl");
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject("https://api.example.go.kr/items?token=" + restTemplate.getForObject(tokenUrl, String.class), String.class);
    }

    // 리터럴의 호스트 자리를 입력으로 바꿔 넣는다: 식이 "https://…/" 로 시작해도 호스트는 고정이 아니다
    public String hostPlaceholderReplaced(HttpServletRequest request) {
        String tenant = request.getParameter("tenant");
        String path = request.getParameter("path");
        String url = "https://TENANT.api.example.go.kr/v1/".replace("TENANT", tenant) + path;
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(url, String.class);
    }

    public String hostPlaceholderReplacedInline(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject("https://HOST/v1/".replaceAll("HOST", request.getParameter("host")) + "items", String.class);
    }

    // 이어 붙인 뒤에 호스트 자리를 바꾼다
    public String replacedAfterConcat(HttpServletRequest request) {
        String url = ("https://TENANT.api.example.go.kr/v1/" + "items").replace("TENANT", request.getParameter("tenant"));
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(url, String.class);
    }
}
