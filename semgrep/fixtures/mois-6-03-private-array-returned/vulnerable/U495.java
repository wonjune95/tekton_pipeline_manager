package demo;

import java.awt.Color;

// 탐지돼야 하는 경우 (진단가이드 6-3: private 배열을 public 메서드가 그대로 반환). 탐지 위치는 메서드 선언 줄
public class U495 {
    private String[] colors;
    private Color[] userColors;
    private int[] scores = new int[10];
    private static final String[] ROLES = {"admin", "user"};

    // ruleid: mois-6-03-private-array-returned
    public String[] getColors() {
        return colors;
    }

    // ruleid: mois-6-03-private-array-returned
    public Color[] getUserColors() {
        return this.userColors;
    }

    // 초기값이 있는 필드
    // ruleid: mois-6-03-private-array-returned
    public int[] getScores() {
        return scores;
    }

    // private static final 이어도 배열의 원소는 바꿀 수 있다
    // ruleid: mois-6-03-private-array-returned
    public static String[] getRoles() {
        return ROLES;
    }

    // 조건에 따라 그대로 반환
    // ruleid: mois-6-03-private-array-returned
    public String[] colorsOrEmpty(boolean visible) {
        if (visible) {
            return colors;
        }
        return new String[0];
    }

    // 지역 변수에 복사본을 만들었지만 반환은 필드(this.colors)다
    // ruleid: mois-6-03-private-array-returned
    public String[] copyButReturnField() {
        String[] colors = this.colors.clone();
        colors[0] = "";
        return this.colors;
    }
}
