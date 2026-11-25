package demo;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.net.http.HttpRequest;
import javax.servlet.http.HttpServletRequest;
import okhttp3.Request;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestOperations;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.reactive.function.client.WebClient;

// 탐지돼야 하는 경우: 외부 입력 URL 로 서버가 요청을 보냄. sink 마다 한 줄씩
@RestController
public class ProxyController {
    private final RestTemplate restTemplate = new RestTemplate();
    private final RestOperations restOperations = new RestTemplate();
    private final WebClient webClient = WebClient.create();
    private final RestClient restClient = RestClient.create();

    // 진단가이드 예: 요청 파라미터 url 로 연결 (openConnection 은 연결 직전 단계지만 여기서 잡는다)
    public HttpURLConnection connect(HttpServletRequest req) throws IOException {
        URL url = new URL(req.getParameter("url"));
        // ruleid: mois-1-12-ssrf
        return (HttpURLConnection) url.openConnection();
    }

    // 진단가이드 정탐 예: 호스트를 입력받아 이미지를 가져옴
    public InputStream favicon(HttpServletRequest request) throws IOException {
        String host = request.getParameter("host");
        // ruleid: mois-1-12-ssrf
        return new URL("http://" + host + "/favicon.ico").openStream();
    }

    public Object content(HttpServletRequest request) throws IOException {
        URL url = new URL(request.getParameter("url"));
        // ruleid: mois-1-12-ssrf
        return url.getContent();
    }

    @GetMapping("/fetch")
    public String fetch(@RequestParam String target) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(target, String.class);
    }

    // RestTemplate 의 요청 메서드마다 한 줄
    public void restTemplateMethods(HttpServletRequest request, HttpEntity<String> body) {
        String target = request.getParameter("target");
        // ruleid: mois-1-12-ssrf
        ResponseEntity<String> a = restTemplate.getForEntity(target, String.class);
        // ruleid: mois-1-12-ssrf
        String b = restTemplate.postForObject(target, body, String.class);
        // ruleid: mois-1-12-ssrf
        ResponseEntity<String> c = restTemplate.postForEntity(target, body, String.class);
        // ruleid: mois-1-12-ssrf
        URI d = restTemplate.postForLocation(target, body);
        // ruleid: mois-1-12-ssrf
        restTemplate.put(target, body);
        // ruleid: mois-1-12-ssrf
        String e = restTemplate.patchForObject(target, body, String.class);
        // ruleid: mois-1-12-ssrf
        restTemplate.delete(target);
        // ruleid: mois-1-12-ssrf
        Object f = restTemplate.headForHeaders(target);
        // ruleid: mois-1-12-ssrf
        Object g = restTemplate.optionsForAllow(target);
        // ruleid: mois-1-12-ssrf
        ResponseEntity<String> h = restTemplate.exchange(target, HttpMethod.GET, body, String.class);
        // ruleid: mois-1-12-ssrf
        String i = restTemplate.execute(target, HttpMethod.GET, null, null);
        // ruleid: mois-1-12-ssrf
        String j = restOperations.getForObject(target, String.class);
    }

    public void springClients(HttpServletRequest request) {
        String target = request.getParameter("target");
        // ruleid: mois-1-12-ssrf
        webClient.get().uri(target).retrieve();
        // ruleid: mois-1-12-ssrf
        WebClient.create(target).get().retrieve();
        // ruleid: mois-1-12-ssrf
        restClient.get().uri(target).retrieve();
    }

    public void jdkHttpClient(HttpServletRequest request) {
        String target = request.getParameter("target");
        // ruleid: mois-1-12-ssrf
        HttpRequest a = HttpRequest.newBuilder(URI.create(target)).build();
        // ruleid: mois-1-12-ssrf
        HttpRequest b = HttpRequest.newBuilder().uri(URI.create(target)).build();
    }

    public void apacheHttpClient4(HttpServletRequest request) {
        String target = request.getParameter("target");
        // ruleid: mois-1-12-ssrf
        HttpGet get = new HttpGet(target);
        // ruleid: mois-1-12-ssrf
        HttpPost post = new HttpPost(target);
        // ruleid: mois-1-12-ssrf
        HttpPut put = new HttpPut(target);
        // ruleid: mois-1-12-ssrf
        HttpDelete delete = new HttpDelete(target);
    }

    public void apacheHttpClient5(HttpServletRequest request) {
        String target = request.getParameter("target");
        // ruleid: mois-1-12-ssrf
        Object get = new org.apache.hc.client5.http.classic.methods.HttpGet(target);
        // ruleid: mois-1-12-ssrf
        Object post = new org.apache.hc.client5.http.classic.methods.HttpPost(target);
        // ruleid: mois-1-12-ssrf
        Object put = new org.apache.hc.client5.http.classic.methods.HttpPut(target);
        // ruleid: mois-1-12-ssrf
        Object delete = new org.apache.hc.client5.http.classic.methods.HttpDelete(target);
    }

    public void okHttp(HttpServletRequest request, Request.Builder builder) {
        String target = request.getParameter("target");
        // ruleid: mois-1-12-ssrf
        Request a = builder.url(target).build();
        // ruleid: mois-1-12-ssrf
        Request b = new Request.Builder().url(target).build();
    }
}
