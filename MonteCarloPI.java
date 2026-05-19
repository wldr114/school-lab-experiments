import java.util.Random;

public class MonteCarloPI {

    public static void main(String[] args) {

        Random random = new Random();

        int total = 1000000;
        int inCircle = 0;

        for (int i = 0; i < total; i++) {

            double x = random.nextDouble();
            double y = random.nextDouble();

            if (x * x + y * y <= 1) {
                inCircle++;
            }
        }

        double pi = 4.0 * inCircle / total;

        System.out.println("圆周率π的估计值：" + pi);
    }
}