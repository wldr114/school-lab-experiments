import java.util.Random;

public class WaitTime {

    public static void main(String[] args) {

        Random random = new Random();

        int count = 1000000;

        double totalWait = 0;

        for (int i = 0; i < count; i++) {

            // 旅客到站时间（0~30分钟）
            double passenger = random.nextDouble() * 30;

            // 堵车时间（0~30分钟）
            double delay = random.nextDouble() * 30;

            // 汽车到站时间
            double busTime = 40 + delay;

            // 等待时间
            double wait = busTime - passenger;

            totalWait += wait;
        }

        double avg = totalWait / count;

        System.out.println("平均等待时间：" + avg + "分钟");
    }
}