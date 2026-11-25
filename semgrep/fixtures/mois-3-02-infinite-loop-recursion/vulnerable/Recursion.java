package demo;

import java.util.List;
import java.util.Queue;

// 탐지돼야 하는 경우 (진단가이드 3-2: 탈출 조건 없는 재귀, 같은 타입 인자로 자신을 호출, 무한 반복)
public class Recursion {
    private int a;
    private boolean debug;

    // ── 재귀: 인자 0~3개, 직접 호출과 this. 호출 ──

    public void tick() {
        // ruleid: mois-3-02-infinite-loop-recursion
        tick();
    }

    public void tock() {
        // ruleid: mois-3-02-infinite-loop-recursion
        this.tock();
    }

    // 기저 조건 없이 자신을 호출한다
    public int factorial(int n) {
        // ruleid: mois-3-02-infinite-loop-recursion
        return n * factorial(n - 1);
    }

    public int countdown(int n) {
        // ruleid: mois-3-02-infinite-loop-recursion
        return this.countdown(n - 1);
    }

    public void func(int a) {
        this.a = a;
    }

    // 같은 이름·같은 타입(String) 인자로 자신을 호출한다 (정탐 예)
    public void func(String a) {
        // ruleid: mois-3-02-infinite-loop-recursion
        func(a);
    }

    public int pad(int width, String text) {
        // ruleid: mois-3-02-infinite-loop-recursion
        return pad(width, text);
    }

    public int padThis(int width, String text) {
        // ruleid: mois-3-02-infinite-loop-recursion
        return this.padThis(width, text);
    }

    public int walk(int depth, String path, List<String> seen) {
        // ruleid: mois-3-02-infinite-loop-recursion
        return walk(depth, path, seen);
    }

    public int walkThis(int depth, String path, List<String> seen) {
        // ruleid: mois-3-02-infinite-loop-recursion
        return this.walkThis(depth, path, seen);
    }

    // ── 기저 조건처럼 보이지만 재귀 호출을 막지 못하는 경우 ──

    // if 가 재귀 호출보다 뒤에 있어 도달하지 못한다
    public int ifAfterCall(int n) {
        // ruleid: mois-3-02-infinite-loop-recursion
        int v = ifAfterCall(n - 1);
        if (n <= 0) {
            return 0;
        }
        return v;
    }

    // 앞의 if 가 함수를 끝내지 않는다 (로그만 남김)
    public int ifWithoutExit(int n) {
        if (debug) {
            a++;
        }
        // ruleid: mois-3-02-infinite-loop-recursion
        return ifWithoutExit(n - 1);
    }

    // if 조건식 안의 호출은 항상 실행된다
    public int callInCondition(int n) {
        // ruleid: mois-3-02-infinite-loop-recursion
        if (callInCondition(n - 1) > 0) {
            a++;
        }
        return a;
    }

    // && 의 왼쪽은 항상 평가된다
    public boolean andLeft(int n) {
        // ruleid: mois-3-02-infinite-loop-recursion
        return andLeft(n - 1) && n > 0;
    }

    // ?: 의 조건 자리는 항상 평가된다
    public int ternaryCondition(int n) {
        // ruleid: mois-3-02-infinite-loop-recursion
        return ternaryCondition(n - 1) > 0 ? 1 : 0;
    }

    // 예외가 날 때까지(StackOverflowError) 끝나지 않는다
    public int insideTry(int n) {
        try {
            // ruleid: mois-3-02-infinite-loop-recursion
            return insideTry(n - 1);
        } catch (RuntimeException e) {
            return 0;
        }
    }

    // ── 무한 반복: while(true) · for(;;) · do-while(true) ──

    // 빠져나오는 문장이 없는 반복문
    public void drain(Queue<String> queue) {
        // ruleid: mois-3-02-infinite-loop-recursion
        while (true) {
            queue.poll();
        }
    }

    public void drainFor(Queue<String> queue) {
        // ruleid: mois-3-02-infinite-loop-recursion
        for (;;) {
            queue.poll();
        }
    }

    public void drainDo(Queue<String> queue) {
        // ruleid: mois-3-02-infinite-loop-recursion
        do {
            queue.poll();
        } while (true);
    }

    // 중괄호 없는 본문
    public void drainNoBrace(Queue<String> queue) {
        // ruleid: mois-3-02-infinite-loop-recursion
        while (true) queue.poll();
    }

    // ── 탈출문처럼 보이지만 바깥 반복문을 끝내지 못하는 경우 ──

    // 안쪽 for 의 break 는 안쪽 반복문만 끝낸다
    public void breakInInnerFor(Queue<String> queue) {
        // ruleid: mois-3-02-infinite-loop-recursion
        while (true) {
            for (int i = 0; i < 3; i++) {
                if (queue.poll() == null) {
                    break;
                }
            }
        }
    }

    public void breakInInnerForEach(List<String> items) {
        // ruleid: mois-3-02-infinite-loop-recursion
        do {
            for (String item : items) {
                if (item.isEmpty()) {
                    break;
                }
            }
        } while (true);
    }

    public void breakInInnerWhile(Queue<String> queue) {
        // ruleid: mois-3-02-infinite-loop-recursion
        for (;;) {
            while (queue.peek() != null) {
                if (queue.poll().isEmpty()) {
                    break;
                }
            }
        }
    }

    public void breakInInnerDo(Queue<String> queue) {
        // ruleid: mois-3-02-infinite-loop-recursion
        for (;;) {
            do {
                if (queue.poll() == null) {
                    break;
                }
            } while (queue.peek() != null);
        }
    }

    // switch 의 break 는 switch 만 끝낸다
    public void breakInSwitch(Queue<Integer> queue) {
        // ruleid: mois-3-02-infinite-loop-recursion
        while (true) {
            switch (queue.size()) {
                case 0:
                    a = 0;
                    break;
                default:
                    queue.poll();
                    break;
            }
        }
    }

    // continue 는 반복을 끝내지 않는다
    public void continueOnly(Queue<String> queue) {
        // ruleid: mois-3-02-infinite-loop-recursion
        while (true) {
            if (queue.poll() == null) {
                continue;
            }
            a++;
        }
    }
}
