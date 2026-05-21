import java.util.Arrays;
import java.util.Scanner;

class ComputerAver {

    public double getAverage(double[] score) {

        double sum = 0;

        for (double s : score) {
            sum += s;
        }

        return sum / score.length;
    }
}

class DelScore {

    private ComputerAver aver;

    public DelScore(ComputerAver aver) {
        this.aver = aver;
    }

    public double deleteScore(double[] score) {

        if (score.length < 3) {
            throw new RuntimeException("评委人数不能少于3人！");
        }

        Arrays.sort(score);

        double[] newScore = new double[score.length - 2];

        for (int i = 1; i < score.length - 1; i++) {
            newScore[i - 1] = score[i];
        }

        return aver.getAverage(newScore);
    }
}

class InputScore {

    private DelScore del;

    public InputScore(DelScore del) {
        this.del = del;
    }

    public double input(double[] score) {

        for (double s : score) {

            if (s < 0 || s > 100) {
                throw new RuntimeException("分数必须在0~100之间！");
            }
        }

        return del.deleteScore(score);
    }
}

class Line {

    private InputScore input;
    private DelScore del;
    private ComputerAver aver;

    public Line() {

        aver = new ComputerAver();

        del = new DelScore(aver);

        input = new InputScore(del);
    }

    public void startWork(double[] score) {

        double result = input.input(score);

        System.out.println("最终平均分：" + result);
    }
}

public class SingerScorePipeline {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        try {
            System.out.println("===== 歌手评分流水线系统 =====");

            System.out.print("请输入评委人数（至少3人）：");
            int n = sc.nextInt();

            if (n < 3) {
                System.out.println("评委人数不能少于3人！程序退出。");
                sc.close();
                return;
            }

            double[] score = new double[n];
            System.out.println("请输入" + n + "位评委的分数（0~100）：");
            for (int i = 0; i < n; i++) {
                System.out.print("评委" + (i + 1) + "：");
                score[i] = sc.nextDouble();
            }

            System.out.print("原始分数：");
            for (double s : score) {
                System.out.print(s + " ");
            }
            System.out.println();

            Line line = new Line();
            line.startWork(score);

        } catch (Exception e) {
            System.out.println("程序出现异常：" + e.getMessage());
        }

        sc.close();
    }
}