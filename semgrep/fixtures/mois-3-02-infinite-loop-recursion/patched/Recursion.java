package demo;

import java.util.List;
import java.util.Queue;

// 탐지되면 안 되는 경우 (진단가이드 3-2 안전한 코드와 오탐 예)
public class Recursion {
    private int a;

    // ── 재귀: 기저 조건이 있다 ──

    // ok: mois-3-02-infinite-loop-recursion — 호출보다 앞의 if 가 return 한다
    public int factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }

    // ok: mois-3-02-infinite-loop-recursion — 호출보다 앞의 if 가 예외를 던진다
    public int checked(int n) {
        if (n < 0) throw new IllegalArgumentException("n");
        return checked(n - 1);
    }

    // ok: mois-3-02-infinite-loop-recursion — 호출이 if 안에 있어 조건이 거짓이면 실행되지 않는다
    public int sumTo(int n) {
        int sum = 0;
        if (n > 0) {
            sum = n + sumTo(n - 1);
        }
        return sum;
    }

    // ok: mois-3-02-infinite-loop-recursion — 호출이 else 안에 있다
    public int sumElse(int n) {
        if (n <= 0) {
            a = 0;
        } else {
            a = n + sumElse(n - 1);
        }
        return a;
    }

    // ok: mois-3-02-infinite-loop-recursion — ?: 의 한쪽 갈래
    public int ternary(int n) {
        return n <= 0 ? 0 : ternary(n - 1);
    }

    // ok: mois-3-02-infinite-loop-recursion — ?: 의 참 쪽 갈래
    public int ternaryYes(int n) {
        return n > 0 ? n + ternaryYes(n - 1) : 0;
    }

    // ok: mois-3-02-infinite-loop-recursion — && 의 오른쪽은 왼쪽이 거짓이면 평가하지 않는다
    public boolean allPositive(int n) {
        return n > 0 && allPositive(n - 1);
    }

    // ok: mois-3-02-infinite-loop-recursion — || 의 오른쪽은 왼쪽이 참이면 평가하지 않는다
    public boolean anyZero(int n) {
        return n <= 0 || anyZero(n - 1);
    }

    // ok: mois-3-02-infinite-loop-recursion — switch 의 case 가 기저 조건
    public int bySwitch(int n) {
        switch (n) {
            case 0:
                return 1;
            default:
                return n * bySwitch(n - 1);
        }
    }

    public void func(int a) {
        this.a = a;
    }

    // ok: mois-3-02-infinite-loop-recursion — 다른 오버로드(int)를 호출하므로 재귀가 아니다 (오탐 예)
    public void func(String a) {
        func(Integer.valueOf(a).intValue());
    }

    // ok: mois-3-02-infinite-loop-recursion — 자식이 없으면 반복문을 돌지 않아 끝난다
    public int depth(Node node) {
        int max = 0;
        for (Node child : node.children) {
            max = Math.max(max, depth(child));
        }
        return max + 1;
    }

    // ok: mois-3-02-infinite-loop-recursion — 횟수가 정해진 for 안의 호출
    public int fanOut(int n) {
        int total = 0;
        for (int i = 0; i < n; i++) {
            total += fanOut(i);
        }
        return total;
    }

    // ok: mois-3-02-infinite-loop-recursion — while 조건이 거짓이면 호출하지 않는다
    public int halve(int n) {
        while (n > 1) {
            n = halve(n - 2);
        }
        return n;
    }

    // ── 반복문: 빠져나오는 문장이 있다 ──

    // ok: mois-3-02-infinite-loop-recursion — 꺼낼 것이 없으면 break
    public int drain(Queue<String> queue) {
        int n = 0;
        while (true) {
            if (queue.poll() == null) {
                break;
            }
            n++;
        }
        return n;
    }

    // ok: mois-3-02-infinite-loop-recursion — return 으로 끝난다
    public String firstNonEmpty(Queue<String> queue) {
        for (;;) {
            String s = queue.poll();
            if (s == null || !s.isEmpty()) {
                return s;
            }
        }
    }

    // ok: mois-3-02-infinite-loop-recursion — 예외로 끝난다
    public void untilEmpty(Queue<String> queue) {
        do {
            if (queue.poll() == null) {
                throw new IllegalStateException("empty");
            }
        } while (true);
    }

    // ok: mois-3-02-infinite-loop-recursion — 레이블 break 는 안쪽 반복문에서도 바깥 반복문을 끝낸다
    public void labeled(Queue<String> queue) {
        outer:
        while (true) {
            for (int i = 0; i < 3; i++) {
                if (queue.poll() == null) {
                    break outer;
                }
            }
        }
    }

    // ok: mois-3-02-infinite-loop-recursion — switch 안의 return 은 반복문도 끝낸다
    public int untilZero(Queue<Integer> queue) {
        while (true) {
            switch (queue.size()) {
                case 0:
                    return 0;
                default:
                    queue.poll();
            }
        }
    }

    // ok: mois-3-02-infinite-loop-recursion — 조건이 있는 반복문
    public void bounded(Queue<String> queue) {
        while (!queue.isEmpty()) {
            queue.poll();
        }
    }

    static final class Node {
        private final List<Node> children;

        Node(List<Node> children) {
            this.children = children;
        }
    }
}
