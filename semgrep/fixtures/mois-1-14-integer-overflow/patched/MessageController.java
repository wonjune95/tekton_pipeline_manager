package demo;

import javax.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지되면 안 되는 경우: 배열 크기로 쓰기 전에 상한을 검사한다 (넘으면 중단하거나, 범위 안일 때만 사용)
@RestController
public class MessageController {
    private static final Logger log = LoggerFactory.getLogger(MessageController.class);
    private static final int MAX_PARAMS = 100;
    private static final int MAX_KB = 64;

    // 진단가이드 안전한 코드 예: 범위를 벗어나면 예외로 중단
    public String[] params(HttpServletRequest request) {
        int paramCt = Integer.parseInt(request.getParameter("slf_msg_param_num"));
        if (paramCt < 0 || paramCt > MAX_PARAMS) {
            throw new IllegalArgumentException("잘못된 입력입니다.");
        }
        // ok: mois-1-14-integer-overflow — 상한을 넘으면 위에서 끝난다
        return new String[paramCt];
    }

    @GetMapping("/buffer")
    public byte[] buffer(@RequestParam int size) {
        if (size < 1 || size >= MAX_KB) {
            String reason = "잘못된 크기입니다.";
            throw new IllegalArgumentException(reason);
        }
        // ok: mois-1-14-integer-overflow — 실패 분기의 마지막 문장이 throw
        return new byte[size * 1024];
    }

    @GetMapping("/thumbnails")
    public byte[][] thumbnails(@RequestParam int count) {
        if (count > MAX_PARAMS) {
            log.warn("too many thumbnails requested");
            return new byte[0][];
        }
        // ok: mois-1-14-integer-overflow — 실패 분기의 마지막 문장이 return
        return new byte[count][];
    }

    // 상한만 먼저 검사하는 형태, 중괄호 없는 if, 상수를 왼쪽에 둔 비교
    @GetMapping("/rows")
    public String[] rows(@RequestParam int rows) {
        if (MAX_PARAMS < rows) return new String[0];
        // ok: mois-1-14-integer-overflow
        return new String[rows];
    }

    @GetMapping("/cols")
    public String[] cols(@RequestParam int cols) {
        if (MAX_PARAMS <= cols) throw new IllegalArgumentException("잘못된 크기입니다.");
        // ok: mois-1-14-integer-overflow
        return new String[cols];
    }

    // 범위 안일 때만 사용한다
    @GetMapping("/cells")
    public int[] cells(@RequestParam int count) {
        if (count >= 0 && count <= MAX_PARAMS) {
            // ok: mois-1-14-integer-overflow — 통과한 분기 안에서만 사용
            return new int[count];
        }
        return new int[0];
    }

    @GetMapping("/slots")
    public int[] slots(@RequestParam int count) {
        if (count < MAX_PARAMS) return new int[count];
        return new int[0];
    }

    @GetMapping("/pages")
    public int[] pages(@RequestParam int count) {
        if (0 < count && MAX_PARAMS > count) {
            return new int[count];
        }
        return new int[0];
    }

    @GetMapping("/lines")
    public int[] lines(@RequestParam int count) {
        if (MAX_PARAMS >= count) {
            return new int[count];
        }
        return new int[0];
    }

    // 상한을 정하는 함수의 반환값을 쓴다
    @GetMapping("/chunk")
    public byte[] chunk(@RequestParam int size) {
        // ok: mois-1-14-integer-overflow — Math.min 으로 상한 고정
        return new byte[Math.min(size, MAX_KB) * 1024];
    }

    @GetMapping("/window")
    public byte[] window(@RequestParam int size) {
        int clamped = Math.clamp(size, 1, MAX_KB);
        // ok: mois-1-14-integer-overflow — Math.clamp 로 범위 고정
        return new byte[clamped];
    }

    // 초기화 목록으로 만드는 배열은 크기를 입력이 정하지 않는다
    public Object[] args(HttpServletRequest request) {
        // ok: mois-1-14-integer-overflow — new T[] {…}
        return new Object[] {request.getParameter("a"), request.getParameter("b")};
    }
}
