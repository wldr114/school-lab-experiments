import java.util.Arrays;
import java.util.Scanner;

interface LineUpStrategy {
    void arrange(int[] a);
}

class StrategyA implements LineUpStrategy {

    public void arrange(int[] a) {

        Arrays.sort(a); // 从小到大
    }
}

class StrategyB implements LineUpStrategy {

    public void arrange(int[] a) {

        // 冒泡排序：从大到小
        for (int i = 0; i < a.length - 1; i++) {
            for (int j = 0; j < a.length - i - 1; j++) {
                if (a[j] < a[j + 1]) {
                    int temp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = temp;
                }
            }
        }
    }
}

class StrategyC implements LineUpStrategy {

    public void arrange(int[] a) {

        int[] temp = new int[a.length];
        int index = 0;

        // 先放奇数
        for (int num : a) {
            if (num % 2 != 0) {
                temp[index++] = num;
            }
        }

        // 再放偶数
        for (int num : a) {
            if (num % 2 == 0) {
                temp[index++] = num;
            }
        }

        // 拷贝回原数组
        for (int i = 0; i < a.length; i++) {
            a[i] = temp[i];
        }
    }
}

class Army {

    private LineUpStrategy strategy;

    public void setStrategy(LineUpStrategy strategy) {
        this.strategy = strategy;
    }

    public void execute(int[] a) {

        strategy.arrange(a);

        System.out.println("列队结果：");
        for (int num : a) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
}

public class MilitaryFormationStrategy {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("===== 军队列队策略系统 =====");

        System.out.print("请输入士兵人数：");
        int n = sc.nextInt();

        int[] soldiers = new int[n];
        System.out.println("请输入" + n + "个士兵的身高（cm）：");
        for (int i = 0; i < n; i++) {
            System.out.print("士兵" + (i + 1) + "身高：");
            soldiers[i] = sc.nextInt();
        }

        Army army = new Army();

        System.out.println("\n请选择列队策略：");
        System.out.println("  1 - 策略A：从低到高");
        System.out.println("  2 - 策略B：从高到低");
        System.out.println("  3 - 策略C：奇偶分组");
        System.out.println("  4 - 全部演示");
        System.out.print("请输入选择：");
        int choice = sc.nextInt();

        switch (choice) {
            case 1:
                System.out.println("\n===策略A：从低到高===");
                army.setStrategy(new StrategyA());
                army.execute(soldiers.clone());
                break;
            case 2:
                System.out.println("\n===策略B：从高到低===");
                army.setStrategy(new StrategyB());
                army.execute(soldiers.clone());
                break;
            case 3:
                System.out.println("\n===策略C：奇偶分组===");
                army.setStrategy(new StrategyC());
                army.execute(soldiers.clone());
                break;
            case 4:
                System.out.println("\n===策略A：从低到高===");
                army.setStrategy(new StrategyA());
                army.execute(soldiers.clone());

                System.out.println("\n===策略B：从高到低===");
                army.setStrategy(new StrategyB());
                army.execute(soldiers.clone());

                System.out.println("\n===策略C：奇偶分组===");
                army.setStrategy(new StrategyC());
                army.execute(soldiers.clone());
                break;
            default:
                System.out.println("输入无效！");
        }

        sc.close();
    }
}