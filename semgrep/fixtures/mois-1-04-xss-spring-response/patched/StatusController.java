package demo;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Map;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지되면 안 되는 경우: 브라우저가 HTML 로 해석하지 않는 응답
@RestController
public class StatusController {
    private final ObjectMapper objectMapper = new ObjectMapper();

    // 응답 형식을 text/plain 으로 지정하면 브라우저가 HTML 로 해석하지 않는다
    @GetMapping(value = "/status", produces = "text/plain;charset=UTF-8")
    public String status(@RequestParam("job") String job) {
        // ok: mois-1-04-xss-spring-response — produces 가 text/plain
        return "job=" + job;
    }

    @GetMapping(value = "/status.txt", produces = MediaType.TEXT_PLAIN_VALUE)
    public String statusText(@RequestParam("job") String job) {
        // ok: mois-1-04-xss-spring-response
        return "job=" + job;
    }

    @GetMapping(value = "/status.json", produces = "application/json")
    public String statusJson(@RequestParam("job") String job) throws JsonProcessingException {
        // ok: mois-1-04-xss-spring-response — produces 가 JSON
        return objectMapper.writeValueAsString(Map.of("job", job));
    }

    @GetMapping(path = "/status2.json", produces = MediaType.APPLICATION_JSON_VALUE)
    public String statusJsonConstant(@RequestParam("job") String job) throws JsonProcessingException {
        // ok: mois-1-04-xss-spring-response
        return objectMapper.writeValueAsString(Map.of("job", job));
    }

    // 내려받기로 응답하면 브라우저가 화면에 그리지 않는다
    @GetMapping(value = "/status.csv", produces = "application/octet-stream")
    public String statusCsv(@RequestParam("job") String job) {
        // ok: mois-1-04-xss-spring-response — produces 가 application/octet-stream
        return "job,state\n" + job + ",done\n";
    }

    @GetMapping(value = "/status.bin", produces = MediaType.APPLICATION_OCTET_STREAM_VALUE)
    public String statusDownload(@RequestParam("job") String job) {
        // ok: mois-1-04-xss-spring-response
        return "job,state\n" + job + ",done\n";
    }

    // 객체를 반환하면 JSON 으로 직렬화된다 (문자열 반환 핸들러만 본다)
    @GetMapping("/status/detail")
    public Map<String, String> detail(@RequestParam("job") String job) {
        // ok: mois-1-04-xss-spring-response
        return Map.of("job", job);
    }

    // 입력은 선택에만 쓰고 응답은 상수
    @GetMapping("/status/label")
    public String label(@RequestParam("job") String job) {
        // ok: mois-1-04-xss-spring-response
        return "batch".equals(job) ? "<b>배치</b>" : "<b>일반</b>";
    }
}
