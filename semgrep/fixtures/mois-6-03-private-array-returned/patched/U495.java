package demo;

import java.util.Arrays;

// 탐지되면 안 되는 경우 (진단가이드 6-3 안전한 코드와 오탐 예: 복사본 반환, public static final 상수)
public class U495 {
    // ok: mois-6-03-private-array-returned — private 이 아닌 공개 상수는 이 항목의 대상이 아니다
    public static final String[] XML_TAG = {"<?xml version=\"1.0\" encoding=\"", "\"?>"};
    private String[] colors;
    private int[] scores = new int[10];

    // ok: mois-6-03-private-array-returned — 새 배열에 복사해 반환
    public String[] getColors() {
        String[] ret = new String[0];
        if (this.colors != null) {
            ret = new String[colors.length];
            for (int i = 0; i < colors.length; i++) {
                ret[i] = this.colors[i];
            }
        }
        return ret;
    }

    // ok: mois-6-03-private-array-returned — 필드와 같은 이름의 지역 배열(복사본)을 반환
    public String[] copyColors() {
        String[] colors = new String[this.colors.length];
        System.arraycopy(this.colors, 0, colors, 0, colors.length);
        return colors;
    }

    // ok: mois-6-03-private-array-returned — Arrays.copyOf·clone 으로 만든 복사본
    public int[] getScores() {
        return Arrays.copyOf(scores, scores.length);
    }

    public int[] cloneScores() {
        return this.scores.clone();
    }

    public static String[] getXmlTag() {
        return XML_TAG;
    }

    // ok: mois-6-03-private-array-returned — public 이 아닌 메서드
    String[] colorsInternal() {
        return colors;
    }

    private int[] scoresInternal() {
        return this.scores;
    }
}
