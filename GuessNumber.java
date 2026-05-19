import java.util.Random;
import java.util.Scanner;

public class GuessNumber {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        Random random = new Random();

        int score = 0;

        while (true) {

            System.out.println("===== 猜数游戏 =====");
            System.out.println("1. 开始");
            System.out.println("2. 退出");

            int choice = sc.nextInt();

            if (choice == 2) {
                System.out.println("游戏结束！");
                break;
            }

            int number = random.nextInt(100);

            int count = 0;
            boolean flag = false;

            while (count < 3) {

                System.out.println("当前得分：" + score);
                System.out.print("请输入你猜的数：");

                int guess = sc.nextInt();

                count++;

                if (guess == number) {

                    System.out.println("你猜对了！");

                    if (count == 1) {
                        score += 3;
                    } else if (count == 2) {
                        score += 2;
                    } else {
                        score += 1;
                    }

                    flag = true;
                    break;

                } else if (guess > number) {

                    System.out.println("太大了！");

                } else {

                    System.out.println("太小了！");
                }
            }

            if (!flag) {

                System.out.println("三次机会已用完！");
                System.out.println("正确数字：" + number);

                score -= 2;
            }

            System.out.println("当前总得分：" + score);
        }
    }
}