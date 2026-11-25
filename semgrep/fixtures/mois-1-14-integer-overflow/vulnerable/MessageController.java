package demo;

import javax.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.MatrixVariable;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지돼야 하는 경우: 외부 입력값을 범위 검사 없이 배열 크기로 사용
@RestController
public class MessageController {
    // 진단가이드 예: 요청 파라미터를 정수로 바꿔 그대로 배열 크기로 쓴다
    public String[] params(HttpServletRequest request) {
        String tmp = request.getParameter("slf_msg_param_num");
        int paramCt = Integer.parseInt(tmp);
        // ruleid: mois-1-14-integer-overflow
        return new String[paramCt];
    }

    // 정수형 Spring 파라미터 (애너테이션에 인자가 없는 형태)
    @GetMapping("/buffer")
    public byte[] buffer(@RequestParam int size) {
        // ruleid: mois-1-14-integer-overflow
        return new byte[size * 1024];
    }

    // 정수형 Spring 파라미터 (애너테이션에 인자가 있는 형태, 래퍼 타입)
    @GetMapping("/rows")
    public String[] rows(@RequestParam("rows") Integer rows) {
        // ruleid: mois-1-14-integer-overflow
        return new String[rows];
    }

    @GetMapping("/blocks/{count}")
    public long[] blocks(@PathVariable long count) {
        // ruleid: mois-1-14-integer-overflow
        return new long[(int) count];
    }

    // 헤더·쿠키·행렬 변수로 받은 정수 (short·Long·Short)
    @GetMapping("/batch")
    public byte[] batch(@RequestHeader("X-Batch-Size") short batchSize) {
        // ruleid: mois-1-14-integer-overflow
        return new byte[batchSize];
    }

    @GetMapping("/page")
    public String[] page(@CookieValue("pageSize") Long pageSize) {
        // ruleid: mois-1-14-integer-overflow
        return new String[pageSize.intValue()];
    }

    @GetMapping("/tree/{path}")
    public int[] tree(@MatrixVariable("depth") Short depth) {
        // ruleid: mois-1-14-integer-overflow
        return new int[depth];
    }

    // 다차원 배열: 어느 차원이든 입력이 크기를 정하면 탐지
    @GetMapping("/grid")
    public int[][] grid(@RequestParam int rows, @RequestParam int cols) {
        // ruleid: mois-1-14-integer-overflow
        int[][] byRows = new int[rows][8];
        // ruleid: mois-1-14-integer-overflow
        int[][] byCols = new int[8][cols];
        // ruleid: mois-1-14-integer-overflow
        int[][] jagged = new int[rows][];
        return byRows.length > 0 ? byCols : jagged;
    }
}
