import java.util.Random;

public class ArrayDemo {

    public static void main(String[] args) {

        int[][] arr = new int[5][5];
        Random random = new Random();

        // 生成随机数
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                arr[i][j] = random.nextInt(100);
            }
        }

        // 输出二维数组
        System.out.println("二维数组内容：");

        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                System.out.print(arr[i][j] + "\t");
            }
            System.out.println();
        }

        // 求最外圈元素之和
        int sum = 0;

        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {

                if (i == 0 || i == 4 || j == 0 || j == 4) {
                    sum += arr[i][j];
                }
            }
        }

        System.out.println("最外圈元素之和：" + sum);

        // 求主对角线最大值
        int max = arr[0][0];
        int index = 0;

        for (int i = 0; i < 5; i++) {

            if (arr[i][i] > max) {
                max = arr[i][i];
                index = i;
            }
        }

        System.out.println("主对角线最大值：" + max);
        System.out.println("位置：[" + index + "][" + index + "]");
    }
}